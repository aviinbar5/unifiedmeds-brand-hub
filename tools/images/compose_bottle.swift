// Put one of our flat labels onto the amber bottle render, keeping the bottle's light.
//
// usage: swift tools/compose_bottle.swift <bottle.png> <designer-flat-label.png> <our-label.png> <out.png>
//
// <bottle.png>               the bottle render exported from the website Figma (read only)
// <designer-flat-label.png>  the flat label that is printed on that bottle (Figma export)
// <our-label.png>            the label to put on instead (assets/packaging/label-*.png, same 560 x 640 layout)
//
// 1. Finds where the flat label sits on the bottle (the Deep Teal label area, then a
//    small search over position and scale that best matches the designer label).
// 2. Shading = blurred brightness of the bottle / blurred brightness of the designer label.
// 3. Writes our label, scaled to the same place and multiplied by that shading.
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

struct Img { var w: Int; var h: Int; var px: [Float] } // RGBA 0...1, premultiplied off

func load(_ path: String) -> Img {
    let url = URL(fileURLWithPath: path) as CFURL
    guard let src = CGImageSourceCreateWithURL(url, nil), let cg = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("cannot read \(path)") }
    let w = cg.width, h = cg.height
    var bytes = [UInt8](repeating: 0, count: w * h * 4)
    let ctx = CGContext(data: &bytes, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
    var px = [Float](repeating: 0, count: w * h * 4)
    for i in 0..<(w * h) {
        let a = Float(bytes[i * 4 + 3]) / 255
        for c in 0..<3 { px[i * 4 + c] = a > 0 ? min(1, Float(bytes[i * 4 + c]) / 255 / a) : 0 }
        px[i * 4 + 3] = a
    }
    return Img(w: w, h: h, px: px)
}

func save(_ img: Img, _ path: String) {
    var bytes = [UInt8](repeating: 0, count: img.w * img.h * 4)
    for i in 0..<(img.w * img.h) {
        let a = img.px[i * 4 + 3]
        for c in 0..<3 { bytes[i * 4 + c] = UInt8(max(0, min(255, (img.px[i * 4 + c] * a * 255).rounded()))) }
        bytes[i * 4 + 3] = UInt8(max(0, min(255, (a * 255).rounded())))
    }
    let ctx = CGContext(data: &bytes, width: img.w, height: img.h, bitsPerComponent: 8, bytesPerRow: img.w * 4, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    let cg = ctx.makeImage()!
    let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(dest, cg, nil)
    CGImageDestinationFinalize(dest)
}

// bilinear sample of a flat label at (x, y) in label pixels
func sample(_ im: Img, _ x: Float, _ y: Float, _ c: Int) -> Float {
    let fx = max(0, min(Float(im.w - 1), x)), fy = max(0, min(Float(im.h - 1), y))
    let x0 = Int(fx), y0 = Int(fy), x1 = min(im.w - 1, x0 + 1), y1 = min(im.h - 1, y0 + 1)
    let dx = fx - Float(x0), dy = fy - Float(y0)
    func p(_ xx: Int, _ yy: Int) -> Float { im.px[(yy * im.w + xx) * 4 + c] }
    return (p(x0, y0) * (1 - dx) + p(x1, y0) * dx) * (1 - dy) + (p(x0, y1) * (1 - dx) + p(x1, y1) * dx) * dy
}
func lum(_ r: Float, _ g: Float, _ b: Float) -> Float { 0.2126 * r + 0.7152 * g + 0.0722 * b }

let args = CommandLine.arguments
guard args.count == 5 else { print("usage: compose_bottle <bottle> <designer-label> <our-label> <out>"); exit(1) }
let bottle = load(args[1]), dLabel = load(args[2]), ours = load(args[3])

// 1a. rough box: pixels close to the label ground (sampled from the designer label corner area)
let gx = 20, gy = 300
let gr = dLabel.px[(gy * dLabel.w + gx) * 4], gg = dLabel.px[(gy * dLabel.w + gx) * 4 + 1], gb = dLabel.px[(gy * dLabel.w + gx) * 4 + 2]
var rowCount = [Int](repeating: 0, count: bottle.h), hit = [Bool](repeating: false, count: bottle.w * bottle.h)
for y in 0..<bottle.h { for x in 0..<bottle.w {
    let i = (y * bottle.w + x) * 4
    if bottle.px[i + 3] > 0.9 && abs(bottle.px[i] - gr) + abs(bottle.px[i + 1] - gg) + abs(bottle.px[i + 2] - gb) < 0.12 { rowCount[y] += 1; hit[y * bottle.w + x] = true }
}}
// the label is the tallest run of rows that are mostly label ground (the cap is shorter)
let peak = rowCount.max() ?? 0
var runs: [(Int, Int)] = []; var s0 = -1
for y in 0..<bottle.h { if rowCount[y] > peak / 5 { if s0 < 0 { s0 = y } } else if s0 >= 0 { runs.append((s0, y - 1)); s0 = -1 } }
if s0 >= 0 { runs.append((s0, bottle.h - 1)) }
let band = runs.max(by: { ($0.1 - $0.0) < ($1.1 - $1.0) })!
var minX = bottle.w, maxX = 0
for y in band.0...band.1 { for x in 0..<bottle.w where hit[y * bottle.w + x] { minX = min(minX, x); maxX = max(maxX, x) } }
let minY = band.0, maxY = band.1
print("rough label box", minX, minY, maxX, maxY)

// 1b. refine: x0, y0, sx, sy so that bottle(x0 + u*sx, y0 + v*sy) ~ designer(u, v)
func cost(_ x0: Float, _ y0: Float, _ sx: Float, _ sy: Float) -> Float {
    var e: Float = 0; var n: Float = 0
    var v: Float = 8
    while v < Float(dLabel.h - 8) { var u: Float = 8
        while u < Float(dLabel.w - 8) {
            let bx = Int(x0 + u * sx), by = Int(y0 + v * sy)
            if bx >= 0 && by >= 0 && bx < bottle.w && by < bottle.h {
                let i = (by * bottle.w + bx) * 4
                let a = lum(bottle.px[i], bottle.px[i + 1], bottle.px[i + 2])
                let b = lum(sample(dLabel, u, v, 0), sample(dLabel, u, v, 1), sample(dLabel, u, v, 2))
                e += (a - b) * (a - b); n += 1
            }
            u += 4 }
        v += 4 }
    return e / max(n, 1)
}
// the printed label keeps the flat label's proportions: one scale from the width
let s0w = Float(maxX - minX + 1) / Float(dLabel.w)
var best = (Float(minX), Float(minY), s0w, s0w)
// coarse search of the top edge, then the fine search below
var bestY = best.1, bestYC = Float.greatestFiniteMagnitude
for dy in stride(from: Float(-80), through: 80, by: 2) { let c = cost(best.0, best.1 + dy, s0w, s0w); if c < bestYC { bestYC = c; bestY = best.1 + dy } }
best.1 = bestY
var bestCost = cost(best.0, best.1, best.2, best.3)
for step: Float in [2, 1, 0.5, 0.25] {
    var improved = true
    while improved {
        improved = false
        for (dx, dy, dsx, dsy) in [(step, 0, 0, 0), (-step, 0, 0, 0), (0, step, 0, 0), (0, -step, 0, 0),
                                   (0, 0, step * 0.004, step * 0.004), (0, 0, -step * 0.004, -step * 0.004)] as [(Float, Float, Float, Float)] {
            let c = cost(best.0 + dx, best.1 + dy, best.2 + dsx, best.3 + dsy)
            if c < bestCost { bestCost = c; best = (best.0 + dx, best.1 + dy, best.2 + dsx, best.3 + dsy); improved = true }
        }
    }
}
print("label at", best, "cost", bestCost)

// 2. shading map over the label area
let (x0, y0, sx, sy) = best
let bx0 = max(0, min(minX - 2, Int(x0.rounded(.down)))), by0 = max(0, Int(y0.rounded(.down)))
let bx1 = min(bottle.w - 1, max(maxX + 2, Int((x0 + Float(dLabel.w) * sx).rounded(.up)))), by1 = min(bottle.h - 1, Int((y0 + Float(dLabel.h) * sy).rounded(.up)))
let W = bx1 - bx0 + 1, H = by1 - by0 + 1
var lb = [Float](repeating: 0, count: W * H), ld = [Float](repeating: 0, count: W * H)
for y in 0..<H { for x in 0..<W {
    let i = ((by0 + y) * bottle.w + (bx0 + x)) * 4
    lb[y * W + x] = lum(bottle.px[i], bottle.px[i + 1], bottle.px[i + 2])
    let u = (Float(bx0 + x) - x0) / sx, v = (Float(by0 + y) - y0) / sy
    ld[y * W + x] = lum(sample(dLabel, u, v, 0), sample(dLabel, u, v, 1), sample(dLabel, u, v, 2))
}}
func blur(_ a: [Float], _ r: Int) -> [Float] {
    var t = a, o = a
    for y in 0..<H { for x in 0..<W { var s: Float = 0; var n: Float = 0
        for k in -r...r { let xx = x + k; if xx >= 0 && xx < W { s += a[y * W + xx]; n += 1 } }
        t[y * W + x] = s / n } }
    for y in 0..<H { for x in 0..<W { var s: Float = 0; var n: Float = 0
        for k in -r...r { let yy = y + k; if yy >= 0 && yy < H { s += t[yy * W + x]; n += 1 } }
        o[y * W + x] = s / n } }
    return o
}
// only plain label ground carries the light; text, rules and the capsule are masked out
let gL = lum(gr, gg, gb)
var mask = [Float](repeating: 0, count: W * H), lbm = [Float](repeating: 0, count: W * H)
for k in 0..<(W * H) { if abs(ld[k] - gL) < 0.03 { mask[k] = 1; lbm[k] = lb[k] } }
let r = 18
let bm = blur(mask, r), blbm = blur(lbm, r)
var blb = [Float](repeating: gL, count: W * H)
let bm2 = blur(mask, 60), blbm2 = blur(lbm, 60)
for k in 0..<(W * H) {
    let wide = bm2[k] > 0.01 ? blbm2[k] / bm2[k] : gL
    let near = bm[k] > 0.001 ? blbm[k] / bm[k] : wide
    let t = min(1, bm[k] / 0.25)
    blb[k] = near * t + wide * (1 - t)
}
let bld = [Float](repeating: gL, count: W * H)
// 3. write our label with the bottle's shading
var out = bottle
for y in 0..<H { for x in 0..<W {
    let X = bx0 + x, Y = by0 + y
    let u = (Float(X) - x0) / sx, v = (Float(Y) - y0) / sy
    if v < 0 || v > Float(dLabel.h - 1) { continue }
    var uu = u
    if u < 0 || u > Float(dLabel.w - 1) {
        // the label wraps around the bottle a little further than the flat art: extend its edge column
        if X < minX - 1 || X > maxX + 1 { continue }
        uu = max(0, min(Float(dLabel.w - 1), u))
    }
    let i = (Y * bottle.w + X) * 4
    if bottle.px[i + 3] < 0.5 { continue }
    let shade = max(0.5, min(1.1, (blb[y * W + x] + 0.02) / (bld[y * W + x] + 0.02)))
    // soften the outer pixel row so the label edge stays anti-aliased
    let edge = min(1, max(0, min(v, Float(dLabel.h - 1) - v)) / 1.0)
    for c in 0..<3 {
        let nv = min(1, sample(ours, uu * Float(ours.w) / Float(dLabel.w), v * Float(ours.h) / Float(dLabel.h), c) * shade)
        out.px[i + c] = bottle.px[i + c] * (1 - edge) + nv * edge
    }
}}
save(out, args[4])
print("wrote", args[4])
