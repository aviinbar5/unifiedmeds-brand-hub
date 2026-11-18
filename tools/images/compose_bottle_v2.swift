// Put one of our flat labels onto the amber bottle render, exactly where the render's own label is.
//
// usage: swift tools/compose_bottle_v2.swift <bottle.png> <our-label.png> <out.png>
//
// 1. Finds the render's label as the pixels that are neither the studio ground nor amber glass,
//    inside the label band. Per row it takes the label's left and right edge, so the new label
//    follows the real silhouette (no straight corners over the glass).
// 2. Light: the brightness of the render's plain label ground, smoothed, divided by its average,
//    keeps the cylinder shading and reflections of the original.
// 3. Maps our flat label across each row's width and the band's height, multiplies by the light,
//    and blends a one-pixel soft edge.
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

struct Img { var w: Int; var h: Int; var px: [Float] }
func load(_ path: String) -> Img {
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil)!
    let cg = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    let w = cg.width, h = cg.height
    var b = [UInt8](repeating: 0, count: w * h * 4)
    let ctx = CGContext(data: &b, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
    var px = [Float](repeating: 0, count: w * h * 4)
    for i in 0..<(w * h) { let a = Float(b[i * 4 + 3]) / 255
        for c in 0..<3 { px[i * 4 + c] = a > 0 ? min(1, Float(b[i * 4 + c]) / 255 / a) : 0 }
        px[i * 4 + 3] = a }
    return Img(w: w, h: h, px: px)
}
func save(_ im: Img, _ path: String) {
    var b = [UInt8](repeating: 0, count: im.w * im.h * 4)
    for i in 0..<(im.w * im.h) { let a = im.px[i * 4 + 3]
        for c in 0..<3 { b[i * 4 + c] = UInt8(max(0, min(255, (im.px[i * 4 + c] * a * 255).rounded()))) }
        b[i * 4 + 3] = UInt8(max(0, min(255, (a * 255).rounded()))) }
    let ctx = CGContext(data: &b, width: im.w, height: im.h, bitsPerComponent: 8, bytesPerRow: im.w * 4, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil); CGImageDestinationFinalize(d)
}
func sample(_ im: Img, _ x: Float, _ y: Float, _ c: Int) -> Float {
    let fx = max(0, min(Float(im.w - 1), x)), fy = max(0, min(Float(im.h - 1), y))
    let x0 = Int(fx), y0 = Int(fy), x1 = min(im.w - 1, x0 + 1), y1 = min(im.h - 1, y0 + 1)
    let dx = fx - Float(x0), dy = fy - Float(y0)
    func p(_ a: Int, _ b: Int) -> Float { im.px[(b * im.w + a) * 4 + c] }
    return (p(x0, y0) * (1 - dx) + p(x1, y0) * dx) * (1 - dy) + (p(x0, y1) * (1 - dx) + p(x1, y1) * dx) * dy
}
func lum(_ r: Float, _ g: Float, _ b: Float) -> Float { 0.2126 * r + 0.7152 * g + 0.0722 * b }

let a = CommandLine.arguments
guard a.count == 4 else { print("usage: compose_bottle_v2 <bottle.png> <our-label.png> <out.png>"); exit(1) }
let bottle = load(a[1]), ours = load(a[2])
let W = bottle.w, H = bottle.h
let bg = [bottle.px[0], bottle.px[1], bottle.px[2]]

func isGround(_ i: Int) -> Bool { bottle.px[i + 3] < 0.5 || abs(bottle.px[i] - bg[0]) + abs(bottle.px[i + 1] - bg[1]) + abs(bottle.px[i + 2] - bg[2]) < 0.10 }
func isAmber(_ i: Int) -> Bool { let r = bottle.px[i], g = bottle.px[i + 1], b = bottle.px[i + 2]; return r > g + 0.05 && g >= b - 0.02 && r > 0.12 }

// candidate label pixels
var cand = [Bool](repeating: false, count: W * H)
for k in 0..<(W * H) { let i = k * 4; cand[k] = !isGround(i) && !isAmber(i) }
// label band: rows where candidate run is wide (the cap is shorter and higher up: take the tallest run of wide rows)
var rowCount = [Int](repeating: 0, count: H)
for y in 0..<H { for x in 0..<W where cand[y * W + x] { rowCount[y] += 1 } }
let peak = rowCount.max() ?? 0
var runs: [(Int, Int)] = []; var s0 = -1
for y in 0..<H { if rowCount[y] > peak * 6 / 10 { if s0 < 0 { s0 = y } } else if s0 >= 0 { runs.append((s0, y - 1)); s0 = -1 } }
if s0 >= 0 { runs.append((s0, H - 1)) }
let band = runs.max(by: { ($0.1 - $0.0) < ($1.1 - $1.0) })!
let top = band.0, bot = band.1
// per row edges: first and last candidate pixel (white type may look like the studio ground,
// so the run can be broken inside; everything between the edges is label), then a median over 9 rows
var L0 = [Int](repeating: 0, count: H), R0 = [Int](repeating: 0, count: H)
for y in top...bot {
    var l = -1, r = -1
    for x in 0..<W where cand[y * W + x] { if l < 0 { l = x }; r = x }
    L0[y] = l; R0[y] = r
}
var L = [Int](repeating: -1, count: H), R = [Int](repeating: -1, count: H)
for y in top...bot {
    var ls: [Int] = [], rs: [Int] = []
    for k in max(top, y - 4)...min(bot, y + 4) { ls.append(L0[k]); rs.append(R0[k]) }
    ls.sort(); rs.sort(); L[y] = ls[ls.count / 2]; R[y] = rs[rs.count / 2]
}
print("label band", top, bot, "row 0 edges", L[top], R[top], "mid", L[(top + bot) / 2], R[(top + bot) / 2])

// ground colour of the render's label: the most common dark-teal tone in the band (median of candidates' luminance below 0.35)
var lums: [Float] = []
for y in top...bot { for x in L[y]...max(L[y], R[y]) { let i = (y * W + x) * 4; let l = lum(bottle.px[i], bottle.px[i + 1], bottle.px[i + 2]); if l < 0.35 { lums.append(l) } } }
lums.sort(); let gL = lums.isEmpty ? 0.2 : lums[lums.count / 2]

// light map from plain ground pixels, smoothed (masked box blur, two radii)
let BW = W, BH = bot - top + 1
var m = [Float](repeating: 0, count: BW * BH), v = [Float](repeating: 0, count: BW * BH)
for y in top...bot { for x in 0..<W where cand[y * W + x] && x >= L[y] && x <= R[y] {
    let i = (y * W + x) * 4; let l = lum(bottle.px[i], bottle.px[i + 1], bottle.px[i + 2])
    if abs(l - gL) < 0.05 { m[(y - top) * BW + x] = 1; v[(y - top) * BW + x] = l } } }
func blur(_ a: [Float], _ r: Int) -> [Float] {
    var t = a, o = a
    for y in 0..<BH { var s: Float = 0
        for x in -r...r { if x >= 0 && x < BW { s += a[y * BW + x] } }
        for x in 0..<BW { t[y * BW + x] = s / Float(2 * r + 1)
            let xo = x - r, xi = x + r + 1
            if xo >= 0 { s -= a[y * BW + xo] }; if xi < BW { s += a[y * BW + xi] } } }
    for x in 0..<BW { var s: Float = 0
        for y in -r...r { if y >= 0 && y < BH { s += t[y * BW + x] } }
        for y in 0..<BH { o[y * BW + x] = s / Float(2 * r + 1)
            let yo = y - r, yi = y + r + 1
            if yo >= 0 { s -= t[yo * BW + x] }; if yi < BH { s += t[yi * BW + x] } } }
    return o
}
let m1 = blur(m, 10), v1 = blur(v, 10), m2 = blur(m, 50), v2 = blur(v, 50)

var out = bottle
for y in top...bot {
    let l0 = Float(L[y]), r0 = Float(R[y]); if r0 - l0 < 20 { continue }
    let vv = Float(y - top) / Float(max(1, bot - top)) * Float(ours.h - 1)
    for x in L[y]...R[y] {
        let k = y * W + x; if bottle.px[k * 4 + 3] < 0.5 { continue }
        let i = k * 4, q = (y - top) * BW + x
        let wide = m2[q] > 0.001 ? v2[q] / m2[q] : gL
        let near = m1[q] > 0.001 ? v1[q] / m1[q] : wide
        let t = min(1, m1[q] / 0.3)
        let light = max(0.55, min(1.12, (near * t + wide * (1 - t) + 0.02) / (gL + 0.02)))
        let uu = (Float(x) - l0) / max(1, r0 - l0) * Float(ours.w - 1)
        // soft edge: the outermost pixel on each side and the first/last row blend half
        var e: Float = 1
        if x == L[y] || x == R[y] || y == top || y == bot { e = 0.5 }
        for c in 0..<3 {
            let nv = min(1, sample(ours, uu, vv, c) * light)
            out.px[i + c] = bottle.px[i + c] * (1 - e) + nv * e
        }
    }
}
save(out, a[3])
print("wrote", a[3], "ground lum", gL)
