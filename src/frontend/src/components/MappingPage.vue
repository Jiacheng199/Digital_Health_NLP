<template>
    <el-container>
        <el-header>
            <el-menu :default-active="activeIndex" mode="horizontal" @select="handleSelect">
                <el-menu-item index="1">Mapping System</el-menu-item>
                <el-menu-item index="2">Mappings</el-menu-item>
                <div style="float:right; line-height: 60px; margin-right:20px;">
                    <span style="margin-right:10px">{{ "Hi, "+userinfo.username }}</span>
                    <el-dropdown>
                        <i class="el-icon-user" style="margin-right: 15px"></i>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item>Profile</el-dropdown-item>
                            <el-dropdown-item><div @click="signout">Sign Out</div></el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
            </el-menu>
        </el-header>
        <el-main>
            <el-table 
            :data="mappings.filter(data => !search || data.comment.toLowerCase().includes(search.toLowerCase()))"
            :default-sort = "{prop: 'editdate', order: 'descending'}"
            style="width: 100%"
            border
            stripe>
                <el-table-column align="center" prop="mapid" label="ID"></el-table-column>
                <el-table-column align="center" prop="username" label="Username" width="180" sortable></el-table-column>
                <el-table-column align="center" prop="comment" label="Comment" width="180"></el-table-column>
                <el-table-column align="center" prop="status" label="Status" width="180"
                :filters="[{ text: 'Pending', value: 'Pending' }, { text: 'Completed', value: 'Completed' }]"
                :filter-method="filterTag"
                filter-placement="bottom-end">
                    <template slot-scope="scope">
                        <el-tag
                        :type="scope.row.status === 'Pending' ? 'warning' : 'primary'"
                        disable-transitions>{{scope.row.status}}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column align="center" prop="editdate" label="Created At" sortable></el-table-column>
                <el-table-column align="center" label="Action" width="360">
                    <template slot="header" slot-scope="scope">
                        <el-input v-model="search" size="mini" placeholder="Type to search"/>
                    </template>
                    <template slot-scope="scope">
                        <el-button type="primary" size="mini" @click="viewMapping(scope.row)">View</el-button>
                        <el-button type="success" size="mini" @click="downloadMapping(scope.row)">Download</el-button>
                        <el-button type="danger" size="mini" @click="deleteMapping(scope.row.mapid)">Delete</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-main>
    </el-container>
</template>
  
<script scoped>
import axios from 'axios';
export default {
name: "MappingPage",
created (){
    this.checktoken();
    this.getmappinginfo();
},
data() {
    return {
    activeIndex: '2',
    userinfo: {},
    mappings: [],
    search:''
    };
},
methods: {
    // check token
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
    // get mapping info
    getmappinginfo(){
        const path = 'http://127.0.0.1:5000/getmaps';
        axios.get(path,{
            headers:{
                'Getmapping': 'Bearer ' + this.userinfo['userid']
            }
        })
        .then(response => {
            this.mappings = response.data.map;
        })
        .catch(error => {
            this.mappings=[];
            console.log(error);
        });
    },
    // delete mapping
    deleteMapping(id){
        const path = 'http://127.0.0.1:5000/deletemap/'+id+'/'+this.userinfo['userid'];
        axios.delete(path)
        .then(response => {
            console.log(response.data.message);
            this.getmappinginfo();
        })
        .catch(error => {
            console.log(error);
        });
    },
    // view mapping
    viewMapping(id){
    console.log(id);
    localStorage.setItem('mapid', id.mapid);
    localStorage.setItem('mapuserid', id.userid);
    this.$router.push("/viewmapping");
    },
    // download mapping
    downloadMapping(id)
    {
        axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/download',
            data: {
            file_id: id.mapid,
            userid: id.userid
            },
            responseType: 'blob'
        })
        .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', id.mapid+'.csv')
            document.body.appendChild(link)
            link.click()
        })
    },
    // router change
    handleSelect(key, keyPath) {
    console.log(key, keyPath);
    if (key == 1) this.$router.push("/home");
    else if (key == 2) this.$router.push("/mapping");
    },
    filterTag(value, row) {
        return row.status === value;
    },
}
};
</script>

<style scoped>
.main-content {
display: flex;
justify-content: center;
align-items: center;
position: relative;
width: 100%;
height: 100%;
}
</style>
  