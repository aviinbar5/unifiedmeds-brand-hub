// Lay bottle PNGs (transparent, with their own soft shadow) on a plain studio ground.
// usage: swift tools/place_bottles.swift <out.png> <width> <height> <r,g,b ground 0-255> <bottle.png>[:scale] ...
// Bottles sit side by side, centred, bottoms aligned at 88% of the height; the middle one is drawn last (in front).
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
let out = a[1], W = Int(a[2])!, H = Int(a[3])!
let rgb = a[4].split(separator: ",").map { CGFloat(Double($0)!) / 255 }
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.setFillColor(CGColor(colorSpace: cs, components: [rgb[0], rgb[1], rgb[2], 1])!)
ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
var imgs: [(CGImage, CGFloat)] = []
for spec in a.dropFirst(5) {
    let parts = spec.split(separator: ":"); let s = parts.count > 1 ? CGFloat(Double(parts[1])!) : 1
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: String(parts[0])) as CFURL, nil)!
    imgs.append((CGImageSourceCreateImageAtIndex(src, 0, nil)!, s))
}
let baseH = CGFloat(H) * 0.80
let sizes = imgs.map { (img, s) -> CGSize in let h = baseH * s; return CGSize(width: h * CGFloat(img.width) / CGFloat(img.height), height: h) }
let overlap: CGFloat = imgs.count > 1 ? 0.22 : 0
let total = sizes.reduce(0) { $0 + $1.width } - CGFloat(max(0, imgs.count - 1)) * overlap * (sizes.first?.width ?? 0)
var x = (CGFloat(W) - total) / 2
var rects: [CGRect] = []
for sz in sizes { rects.append(CGRect(x: x, y: CGFloat(H) * 0.04, width: sz.width, height: sz.height)); x += sz.width * (1 - overlap) }
// draw order: outer ones first, middle last
var order = Array(0..<imgs.count)
if imgs.count == 3 { order = [0, 2, 1] }
for i in order { ctx.draw(imgs[i].0, in: rects[i]) }
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, ctx.makeImage()!, nil); CGImageDestinationFinalize(d)
print("wrote", out)
