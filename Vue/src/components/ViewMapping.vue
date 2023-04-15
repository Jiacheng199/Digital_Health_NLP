<template>
    <div>
        <el-menu class="el-menu-demo" mode="horizontal">
            <el-menu-item index="1"><router-link to="/home" style="text-decoration: none;">Mapping System</router-link></el-menu-item>
            <el-menu-item index="2"><router-link to="/home" style="text-decoration: none;">Upload</router-link></el-menu-item>
            <el-menu-item index="3"><router-link to="/mapping" style="text-decoration: none;">Mappings</router-link></el-menu-item>
            <div style="float:right; line-height: 60px; margin-right:20px;">
                <span style="margin-right:10px">{{ "Hi, "+userinfo.username }}</span>
                <el-dropdown>
                    <i class="el-icon-setting" style="margin-right: 15px"></i>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item>Profile</el-dropdown-item>
                        <el-dropdown-item><div @click="signout">Sign Out</div></el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </div>
        </el-menu>
        
        <el-row>
            <el-col :span="12">
                <div class="grid-content bg-purple">
                    <div ref="pieChart" style="height: 400px; width:auto">
                    </div>
                </div>
            </el-col>
            <el-col :span="12">
                <div class="grid-content bg-purple-light">
                    <div ref="sourcepieChart" style="height: 400px; width:auto">
                    </div>
                </div>
            </el-col>
        </el-row>
        <el-row>
            <el-table 
            :data="tableData.filter(data => !search || data.raw.toLowerCase().includes(search.toLowerCase()) || data.result.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%" border height="800" stripe>
            <el-table-column align="center" label="id" prop="index"></el-table-column>
            <el-table-column align="center" label="Raw Text" prop="raw"></el-table-column>
            <el-table-column align="center" label="Target Text" prop="result"></el-table-column>
            <el-table-column align="center" prop="Flag" label="Source" width="120"
            :filters="[{ text: 'SNOMED CT', value: 'SNOMED CT' }, { text: 'UIL', value: 'UIL' }]"
            :filter-method="filterTag"
            filter-placement="bottom-end">
                <template slot-scope="scope">
                    <el-tag
                    :type="scope.row.Flag === 'SNOMED CT' ? 'primary' : 'success'"
                    disable-transitions>{{scope.row.Flag}}</el-tag>
                </template>
            </el-table-column>
            <el-table-column align="center">
                <template slot="header" slot-scope="scope">
                    <el-input v-model="search" size="mini" placeholder="Type to search"/>
                </template>
                <template slot-scope="scope">
                    <el-button size="mini" @click="handleEdit(scope.$index, scope.row); editDialogVisible=true">
                        Edit
                    </el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row); deleteDialogVisible=true">
                        Delete
                    </el-button>
                </template>
            </el-table-column>
            </el-table>
        </el-row>
        <el-dialog title="Edit" :visible.sync="editDialogVisible" width="30%" :before-close="handleClose">
            <el-form :model="form">
                <el-form-item label="Raw Text" :label-width="formLabelWidth">
                    <!-- can add autocomplete later -->
                    <el-input v-model="form.raw" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="Target Text" :label-width="formLabelWidth">
                    <!-- can add autocomplete later -->
                    <el-input v-model="form.result" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="Source" :label-width="formLabelWidth">
                    <el-select v-model="form.Flag">
                        <el-option label="SNOMED CT" value="SNOMED CT"></el-option>
                        <el-option label="UIL" value="UIL"></el-option>
                    </el-select>
                </el-form-item>
                
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editDialogVisible = false; cancelEdit()">Cancel</el-button>
                <el-button type="primary" @click="editDialogVisible = false; editmapping()">Confirm</el-button>
            </span>
        </el-dialog>
        <el-dialog
        title="Warning"
        :visible.sync="deleteDialogVisible"
        width="30%">
            <span>Are you sure want to delete?</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteDialogVisible = false">Cancel</el-button>
                <el-button type="primary" @click="deleteDialogVisible = false; deletemapping()">Confirm</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
var temp = 0;
export default{
    name: "ViewMapping",
    created(){
        this.checktoken();
        // this.getinfo();
        this.getmapresult();
    },
    data(){
        return{
            userinfo: {},
            search: '',
            tableData: [],
            chartData: [
            { value: 0, name: 'no match' },
            { value: 0, name: 'match' },
            ],
            chartData1: [
            { value: 0, name: 'UIL' },
            { value: 0, name: 'SNOMED CT' },
            ],
            // dialog
            editDialogVisible: false,
            deleteDialogVisible: false,
            form: {
                raw: '123',
                result: '',
                Flag: '',
            },
            formLabelWidth: '120px'
            // mapresult: []
        };
    },
    methods: {
        checktoken(event){
            const tokenStr = localStorage.getItem('token');
            if (tokenStr !== null) {
                const tokenObj = JSON.parse(tokenStr);
                const userInfo = tokenObj.userinfo;
                const expireTime = tokenObj.expireTime;

                if (new Date().getTime() > expireTime) {
                    localStorage.removeItem('tokenObj');
                    this.$router.push("/login");
                }
                else this.userinfo = userInfo;
            }
            else{
                this.$router.push("/login");
            }
        },
        // signout
        signout(event){
            localStorage.removeItem('token');
            this.$router.push("/login");
        },
        getmapresult(){
            const tokenStr = localStorage.getItem('token');
            const tokenObj = JSON.parse(tokenStr);
            const path = 'http://127.0.0.1:5000/getmapresult/'+tokenObj.userinfo["userid"] + '/'+localStorage.getItem('mapid');
            axios.get(path)
            .then(response => {
                this.tableData = response.data;
                this.chartData[0].value = 0;
                this.chartData[1].value = 0;
                this.chartData1[0].value = 0;
                this.chartData1[1].value = 0;
                for (var i = 0; i < this.tableData.length; i++){
                    this.tableData[i].index = i;
                    if (this.tableData[i].result == 'Non-Match')
                    {
                        this.chartData[0].value += 1;
                    }
                    else{
                        this.chartData[1].value += 1;
                    }
                    if(this.tableData[i].Flag == 'UIL')
                    {
                        this.chartData1[0].value += 1;
                    }
                    else{
                        this.chartData1[1].value += 1;
                    }
                }
                const pieChart = echarts.init(this.$refs.pieChart);
                const sourcepieChart = echarts.init(this.$refs.sourcepieChart);
                const options = {
                    title: {
                    text: 'Mapping Result',
                    left: 'center',
                    },
                    tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)',
                    },
                    legend: {
                    orient: 'vertical',
                    left: 'left',
                    data: ['match', 'no match'],
                    },
                    series: [
                    {
                        name: 'Mapping Result',
                        type: 'pie',
                        radius: '55%',
                        center: ['50%', '60%'],
                        data: this.chartData,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)',
                            },
                        },
                    },
                    ],
                };
                const sourceoptions = {
                    title: {
                    text: 'Mapping Source',
                    left: 'center',
                    },
                    tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)',
                    },
                    legend: {
                    orient: 'vertical',
                    left: 'left',
                    data: ['UIL', 'SNOMED CT'],
                    },
                    series: [
                    {
                        name: 'Mapping Source',
                        type: 'pie',
                        radius: '55%',
                        center: ['50%', '60%'],
                        data: this.chartData1,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)',
                            },
                        },
                    },
                    ],
                    color:['#68b8d9','#f9c14e']
                };
                sourcepieChart.setOption(sourceoptions);
                pieChart.setOption(options);
            })
            .catch(error => {
                console.log(error);
            });
        },
        handleEdit(index, row) {
            this.form = row;
            console.log(index, row);
        },
        handleDelete(index, row) {
            this.form = row;
            console.log(index, row);
        },
        filterTag(value, row) {
            return row.Flag === value;
        },
        indexMethod(index) {
            return index+1;
        },
        // dialog
        handleClose(done) {
            this.$confirm('Are you sure to cancel the edit?')
            .then(_ => {
                this.cancelEdit();
                done();
            })
            .catch(_ => {});
            
        },
        cancelEdit(event){
            this.getmapresult();
            // const path = 'http://127.0.0.1:5000/getmapresult/'+localStorage.getItem('userid') + '/'+localStorage.getItem('mapid');
            // axios.get(path)
            // .then(response => {
            //     this.tableData = response.data;
            // })
            // .catch(error => {
            //     console.log(error);
            // });
        },
        editmapping(event){
            const path = 'http://127.0.0.1:5000/editmapping';
            axios.post(path, {
                editinfo: this.form,
                userid: this.userinfo["userid"],
                mapid: localStorage.getItem('mapid')
            })
            .then(response => {
                console.log(response.data.message);
                this.getmapresult();
            })
            .catch(error => {
                console.log(error);
            });
        },
        deletemapping(event){
            const path = 'http://127.0.0.1:5000/deletemapping';
            axios.post(path, {
                mapinfo: this.form,
                userid: this.userinfo["userid"],
                mapid: localStorage.getItem('mapid')
            })
            .then(response => {
                console.log(response.data.message);
                this.getmapresult();
            })
            .catch(error => {
                console.log(error);
            });
        }
    }
}

</script>

<style>
</style>

