// Make the flat studio background of a bottle render transparent, keeping its soft shadow.
//
// usage: swift tools/key_background.swift <in.png> <out.png>
//
// The background colour is read from the top-left pixel. Every pixel connected to the image
// border whose colour is close to it (the ground and the soft shadow) becomes "colour to alpha":
// the ground turns fully transparent, the shadow turns into a translucent dark. The bottle,
// which is not connected to the border through near-ground pixels, is left as it is.
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 3 else { print("usage: key_background <in.png> <out.png>"); exit(1) }
let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!
let cg = CGImageSourceCreateImageAtIndex(src, 0, nil)!
let w = cg.width, h = cg.height
var px = [UInt8](repeating: 0, count: w * h * 4)
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
let ctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))

let B = [Float(px[0]), Float(px[1]), Float(px[2])]
func dist(_ i: Int) -> Float { abs(Float(px[i]) - B[0]) + abs(Float(px[i + 1]) - B[1]) + abs(Float(px[i + 2]) - B[2]) }

// flood fill from the border through near-ground pixels
let tol: Float = 75
var inBg = [Bool](repeating: false, count: w * h)
var stack: [Int] = []
for x in 0..<w { stack.append(x); stack.append((h - 1) * w + x) }
for y in 0..<h { stack.append(y * w); stack.append(y * w + w - 1) }
while let k = stack.popLast() {
    if inBg[k] || dist(k * 4) > tol { continue }
    inBg[k] = true
    let x = k % w, y = k / w
    if x > 0 { stack.append(k - 1) }; if x < w - 1 { stack.append(k + 1) }
    if y > 0 { stack.append(k - w) }; if y < h - 1 { stack.append(k + w) }
}

// colour to alpha (towards black for anything darker than the ground)
var out = [UInt8](repeating: 0, count: w * h * 4)
for k in 0..<(w * h) {
    let i = k * 4
    if !inBg[k] { for c in 0..<4 { out[i + c] = px[i + c] }; continue }
    // alpha so that p = alpha * colour + (1 - alpha) * B, with colour as dark as needed
    var al: Float = 0
    for c in 0..<3 { let p = Float(px[i + c]), b = B[c]
        let ac = p < b ? (b - p) / b : (p - b) / (255 - b + 0.001)
        al = max(al, ac) }
    al = min(1, al)
    if al < 0.02 { continue }
    for c in 0..<3 { let p = Float(px[i + c]), b = B[c]
        let col = (p - (1 - al) * b) / al
        out[i + c] = UInt8(max(0, min(255, (col * al).rounded()))) } // premultiplied
    out[i + 3] = UInt8((al * 255).rounded())
}
let octx = CGContext(data: &out, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, octx.makeImage()!, nil)
CGImageDestinationFinalize(dest)
print("wrote", a[2], "ground", B)
