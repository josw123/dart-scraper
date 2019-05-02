<template>
    <div class="dart-form">
        <el-form label-width="100px">
            <el-form-item label="API KEY">
                <el-input
                    placeholder="Please enter your api key "
                    v-model="mAPIKey"
                    :disabled="mAPIKeyReady" 
                    style="width: 500px;"
                >
                    <el-button slot="append" icon="el-icon-setting" @click="setDartAPIKey"></el-button>
                </el-input>
            </el-form-item>
            <el-form-item label="Company">
                <el-select
                    v-model="mSelectedCrp"
                    multiple
                    filterable
                    remote
                    reserve-keyword
                    placeholder="Please enter a company name"
                    :remote-method="searchName"
                    :loading="mLoading"
                    :disabled="mAPIKeyValid"
                    style="width: 500px;"
                >
                    <el-option
                            v-for="item in mSearchedCrp"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="Data Range">
                <el-date-picker
                    v-model="mDataRange"
                    type="monthrange"
                    range-separator="To"
                    start-placeholder="Start date"
                    end-placeholder="End date"
                    value-format="yyyyMMdd"
                    :disabled="mAPIKeyValid"
                    style="width:500px"
                >
                </el-date-picker>
            </el-form-item>
            <el-form-item label="Report Type">
                <el-select 
                    v-model="mReportTp" 
                    :disabled="mAPIKeyValid"
                    placeholder="Select" 
                    style="width:240px; margin-right: 5px"
                >
                    <el-option
                        v-for="item in mReportOption"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                </el-select>
                <el-select 
                    v-model="mSeparate"
                    :disabled="mAPIKeyValid"
                    placeholder="Select"
                    style="width:240px; margin-left: 5px;"
                >
                    <el-option
                            v-for="item in mSeparateOption"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="Save Path">
                <el-input placeholder="Path" v-model="mPath" style="width: 500px;">
                    <el-button slot="append" icon="el-icon-search" @click="setPath"></el-button>
                </el-input>
            </el-form-item>
            <el-form-item style="text-align: left;">
                <el-button
                    type="primary"
                    style="width: 200px;"
                    :loading="mDownloading"
                    @click="extract"
                    :disabled="!mEnableExtract"
                > {{mExtractBtn}} </el-button>
            </el-form-item>
        </el-form>
        <el-input
                ref="output"
                type="textarea"
                :autosize="{ minRows: 7, maxRows: 7}"
                resize="none"
                placeholder="Output"
                :disabled="true"
                v-model="mOutput">
        </el-input>
    </div>
</template>

<script>
    import { Loading } from 'element-ui'
    const { dialog } = require('electron').remote
    const { ipcRenderer } = require('electron')
    
    export default {
        name: "dart-form",
        data () {
            let APIKey = ''
            let APIKeyReady = false             
            let today = new Date()
            let dd = '' + today.getDate()
            dd = (dd.length < 2)? '0' + dd: dd
            let mm = '' + (today.getMonth() + 1)
            mm = (mm.length < 2)? '0' + mm: mm
            let yyyy = '' + today.getFullYear()
            today = `${yyyy}${mm}${dd}`
            return {
                mAPIKey: APIKey,
                mAPIKeyReady: APIKeyReady,
                mSelectedCrp: '',
                mSearchedCrp: [],
                mLastKeyInput: '',
                mLoading: false,
                mDataRange: ['20150101',today],
                mReportOption: [
                    {label: 'Annual', value: 'annual'},
                    {label: 'Half', value: 'half'},
                    {label: 'Quarter', value: 'quarter'}
                ],
                mReportTp: 'annual',
                mSeparateOption: [
                    {label: 'Consolidated', value: "false"},
                    {label: 'Separate', value: "true"}
                ],
                mSeparate: "false",
                mPath:'',
                mExtractBtn: 'Extract',
                mDownloading: false,
                mOutput:''
            }
        },
        methods: {
            setDartAPIKey(){
                if (this.mAPIKeyReady) {
                    this.mAPIKeyReady = false
                    this.mAPIKey = ''
                } else {
                    let arg
                    if (this.mAPIKey.length !== 40) {
                        arg = {'opcode': 'dart_get_api_key', 'data': 'null'}
                    } else {
                        arg = {'opcode': 'dart_set_api_key', 'data': this.mAPIKey}
                    }
                    
                    let loadingInstance = Loading.service({ fullscreen: true })
                    let recv = ipcRenderer.sendSync('ipc-dart-server', arg)

                    if (recv['connected']=== true){
                        if (recv['data'] === "null") {
                            this.$message({
                                showClose: true,
                                message: 'DART API Key is not set',
                                type: 'error'
                            })
                            loadingInstance.close()
                        } else {
                            this.mAPIKeyReady = true
                            this.mAPIKey = recv['data']
                        
                            arg = {'opcode': 'dart_get_crp_list', 'data': 'null'}
                            ipcRenderer.once('ipc-async-end',  (event, arg) => {
                                this.$message({
                                    showClose: true,
                                    message: 'Successfully loaded',
                                    type: 'success'
                                })
                                loadingInstance.close()
                            })
                            ipcRenderer.send('ipc-dart-server-async', arg)
                        }
                    } else {
                        this.$message({
                            showClose: true,
                            message: 'Please try again later ',
                            type: 'error'
                        })
                        loadingInstance.close()
                    }
                }
            },
            searchName(query) {
                if (query.length > 0) {
                    this.mLoading = true
                    this.mLastKeyInput = Date.now()
                    setTimeout(()=> {
                        const currentTime = Date.now()
                        if (currentTime - this.mLastKeyInput > 400){
                            const arg = {'opcode': 'dart_find_by_name', 'data': query}
                            let recv = ipcRenderer.sendSync('ipc-dart-server', arg)
                            let crp_list = recv['data']
                            if (crp_list !== "null") {
                                crp_list = crp_list.slice(1, -1).split(',')
                                const regex = /\[(\d*?)\](.*)/
                                this.mSearchedCrp = crp_list.map(value => {
                                    let res = value.match(regex)
                                    let ret_val
                                    if (res) {
                                        ret_val = {label: res[2], value: res[1]}
                                    } else {
                                        ret_val = null
                                    }
                                    return ret_val
                                })
                            } else {
                                this.mSearchedCrp = []
                            }
                            this.mLoading = false
                        } 
                    }, 500)
                }
            },
            setPath() {
                const prop = {properties: ['openDirectory','createDirectory']}
                let path = dialog.showOpenDialog(prop)
                if (path) {
                    this.mPath = path[0]
                }
            },
            extract() {
                this.mOutput = ''
                this.mExtractBtn = 'Downloading'
                this.mDownloading = true
                let data = {
                    crp_cd_list: this.mSelectedCrp,
                    start_dt: this.mDataRange[0],
                    end_dt: this.mDataRange[1],
                    report_tp: this.mReportTp,
                    separate: this.mSeparate,
                    path: this.mPath
                }
                const arg = {'opcode': 'dart_download_file', 'data': data}

                ipcRenderer.on('console-stdout', (event, arg) => {
                    this.mOutput += arg
                })

                ipcRenderer.on('console-stderr', (event, arg) => {
                    function removeLast(x) {
                        if(x.lastIndexOf("\n")>0) {
                            return x.substring(0, x.lastIndexOf("\n"));
                        } else {
                            return x;
                        }   
                    }
                    let lines = arg.split(/\r\n|\r|\n/g);
                    if (lines.length > 2) {
                        this.mOutput += '\n' + lines[lines.length-1]
                    } else {
                        this.mOutput = removeLast(this.mOutput)
                        this.mOutput += '\n' + lines[lines.length-1]
                    }
                })

                ipcRenderer.once('ipc-async-end', (event, arg) => {
                    ipcRenderer.removeAllListeners('console-stderr')
                    ipcRenderer.removeAllListeners('console-stdout')
                    let opcode = arg['opcode']
                    if (opcode === 'success') {
                        this.mExtractBtn = 'Extract'
                        this.mDownloading = false   
                    }
                })

                ipcRenderer.send('ipc-dart-server-async', arg)
            }
        },
        computed: {
            mAPIKeyValid: function () {
                return !this.mAPIKeyReady && (this.mAPIKey.length !== 40)
            },
            mEnableExtract: function () {
                return (this.mSelectedCrp.length > 0) && (this.mPath.length > 0)
            }
        },
        watch: {
            mOutput: function() {
                this.$refs.output.scrollTop = this.$refs.output.scrollHeight
            }
        }
    }
</script>

<style scoped>
.dart-form {
    padding: 10px;
}
</style>