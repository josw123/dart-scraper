'use strict'

import fs from 'fs'
import net from 'net'
import path from 'path'
import { app, protocol, BrowserWindow } from 'electron'
import {
  createProtocol,
  installVueDevtools
} from 'vue-cli-plugin-electron-builder/lib'
import {spawn} from 'child_process'
import {ipcMain} from 'electron'
import kill from 'tree-kill'
import jschardet from 'jschardet'
import iconv from 'iconv-lite'
import fixPath from 'fix-path'

fixPath()

const isDevelopment = process.env.NODE_ENV !== 'production'

let dartServer

function decodeString(data) {
  let char_tp = jschardet.detect(data)['encoding']
  const char_list = ['ascii', 'UTF-8']
  let console_log = ''
  if (!char_list.includes(char_tp)) {
    console_log = iconv.decode(data, "euc-kr").toString()
  } else {
    console_log = data.toString()
  }
  return console_log
}

function startDartServer() {
  if (dartServer == null) {
    let exec_path
    if (process.platform === 'win32') {
      exec_path = '/../bin/win_server.exe'
    } else if (process.platform === 'darwin') {
      exec_path =  '/../bin/macos_server'
    }
    
    let real_path =  __dirname + exec_path
    if (!fs.existsSync(real_path)) {
      real_path = process.resourcesPath + exec_path
    }
    real_path = path.resolve(real_path)
    dartServer = spawn(real_path)
    dartServer.stdout.on('data', (data) => {
      const regex = /Socket Open/;
      let console_log = decodeString(data)
      let lines = console_log.split(/\r\n|\r|\n/g);
      for (let i in lines) {
        if (regex.test(lines[i])) {
          let port = parseInt(lines[i].match(/\d\d\d\d\d?/)[0])
          connectServer(port)
        }
      }
    })
  }
}

let client

function connectServer(port) {
  client = new net.Socket()
  client.connect(port)
}

function sendMessage(code, infomation, event) {
  if (client) {
    let packet = JSON.stringify({'opcode': code, 'data': infomation})
    client.write(packet)
    client.on('data', function(data) {
      let results = JSON.parse(data)
      event.returnValue = {connected: true, opcode: results['opcode'], data: results['data']}
    })
  } else {
    event.returnValue = {connected: false, opcode: 'error', data: null}
  }
}

ipcMain.on('ipc-dart-server', (event, arg) => {
  let opcode = arg['opcode']
  let data = arg['data']
  sendMessage(opcode, data, event)
})

function appQuit() {
  client.destroy()
  kill(dartServer.pid)
  app.quit()
}

let logger_attached = false

function attached_log() {
  dartServer.stdout.on('data', (data) => {
    let console_log = decodeString(data)
    if (win) {
      win.webContents.send('console-stdout', console_log)
    }
  })

  dartServer.stderr.on('data', (data) => {
    let console_log = decodeString(data)
    if (win) {
      win.webContents.send('console-stderr', console_log)
    }
  })
}

function asyncSendMessage(code, infomation, event) {
  if (client) {
    let packet = JSON.stringify({'opcode': code, 'data': infomation})
    client.write(packet)
    if (!logger_attached) {
      logger_attached = true
      attached_log()
    }
    client.on('data', function(data) {
      let results = JSON.parse(data)
      event.sender.send('ipc-async-end', {connected: true, opcode: results['opcode'], data: results['data']})
    })
  } else {
    event.sender.send('ipc-async-end', {connected: false, opcode: 'error', data: null})
  }
}

ipcMain.on('ipc-dart-server-async', (event, arg) => {
  let opcode = arg['opcode']
  let data = arg['data']
  asyncSendMessage(opcode, data, event)
})

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([{scheme: 'app', secure: true }])

function createWindow () {
  startDartServer()
  // Create the browser window.
  win = new BrowserWindow({
    width: 650,
    height: 800,
    icon: __dirname + 'assets/logo.png',
    webPreferences: {
    nodeIntegration: true
  }})
  win.setResizable(false)
  win.setMenu(null)
  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }
  win.on('closed', () => {
    win = null
  })
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    appQuit()
  }
  appQuit()
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installVueDevtools()
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', data => {
      if (data === 'graceful-exit') {
        appQuit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      appQuit()
    })
  }
}

