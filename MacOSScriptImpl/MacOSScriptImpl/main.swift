//
//  main.swift
//  MacOSScriptImpl
//
//  Created by 田述新 on 2021/1/23.
//

import Foundation
import Cocoa
import CoreFoundation
import ApplicationServices



func captureWindowByWindowName(name:String, targetPath:String) -> NSDictionary {
    var windowId:CGWindowID? = nil
    var windowX:Int = 0
    var windowY:Int = 0
    var windowW:Int = 0
    var windowH:Int = 0
    if let info = CGWindowListCopyWindowInfo(.optionOnScreenOnly, kCGNullWindowID) as? [[String:Any]] {
        for dict in info {
            if (dict[kCGWindowOwnerName as String] as! String == name){
                let windowsBounds:NSDictionary = dict[kCGWindowBounds as String] as! NSDictionary
                windowX = windowsBounds["X"] as! Int
                windowY = windowsBounds["Y"] as! Int
                windowW = windowsBounds["Width"] as! Int
                windowH = windowsBounds["Height"] as! Int
                windowId = (dict[kCGWindowNumber as String] as! NSNumber).uint32Value
            }
        }
    }
    if (windowId != nil) {
        let windowImage:CGImage? = CGWindowListCreateImage(.null, .optionIncludingWindow, windowId!, [.boundsIgnoreFraming, .nominalResolution])
        if(windowImage==nil){
            return [:]
        }
        let url:CFURL = NSURL.init(fileURLWithPath: targetPath)
        let destination:CGImageDestination? = CGImageDestinationCreateWithURL(url as CFURL, kUTTypeJPEG, 1, nil)
        if(destination == nil){
            return [:]
        }
        CGImageDestinationAddImage(destination!, windowImage!, nil)
        if(CGImageDestinationFinalize(destination!)){
            return [
                "x":windowX,
                "y":windowY,
                "w":windowW,
                "h":windowH,
            ]
        }
    }
    return [:];
}


func click(x:Int, y:Int) {
    let source = CGEventSource.init(stateID: .hidSystemState)
    let mousePosition: CGPoint = CGPoint(x: x, y: y)
    let mouseEvent = CGEvent(mouseEventSource: source, mouseType: .leftMouseDown,
                             mouseCursorPosition: mousePosition, mouseButton: .left)
    mouseEvent?.post(tap: .cghidEventTap)
    let mouseEventUp = CGEvent(mouseEventSource: source, mouseType: .leftMouseUp,
                               mouseCursorPosition: mousePosition, mouseButton: .left)
    mouseEvent?.post(tap: .cghidEventTap)
    mouseEventUp?.post(tap: .cghidEventTap)
}


func formatToJson(input:NSDictionary)->String?{
    do {
        let jsonData = try JSONSerialization.data(withJSONObject: input)
        return String(data: jsonData, encoding: String.Encoding.ascii)
    } catch {
    }
    return nil
}


func printHelp(){
    print("run with argument 'capture $targetPath $windowName' to capture window by $windowname and sava image to $targetPath")
    print("run with argument 'click $x $y' to send a mouse click enent at ($x, $y)")
}

let arguments = CommandLine.arguments
if (arguments.count > 2) {
    let cmd = arguments[1]
    switch cmd {
    case "capture":
        if (arguments.count != 4) {
            printHelp()
        } else {
            let targetPath = arguments[2]
            let windowName = arguments[3]
            let result = captureWindowByWindowName(name: windowName, targetPath: targetPath)
            print(formatToJson(input: result) ?? "")
        }
    case "click":
        if (arguments.count != 4) {
            printHelp()
        } else {
            let x = Int(arguments[2])
            let y = Int(arguments[3])
            if (x != nil && y != nil) {
                click(x: x!, y: y!)
            }
        }
    default:
        printHelp()
    }
} else {
    printHelp()
}


