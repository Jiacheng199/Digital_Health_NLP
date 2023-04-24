<template>
    <el-container>
        <!-- Nav bar -->
        <el-header>
            <el-menu :default-active="activeIndex" mode="horizontal" @select="handleSelect">
                <!-- Menu items -->
                <el-menu-item index="1">Mapping System</el-menu-item>
                <el-menu-item index="2">Mappings</el-menu-item>
                <!-- Display user name in nav bar -->
                <div style="float:right; line-height: 60px; margin-right:20px;">
                    <span style="margin-right:10px">{{ "Hi, "+userinfo.username }}</span>
                    <!-- Dropdown for sign out and view user profile -->
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
            <!-- table shows all users' mapping tasks -->
            <!-- set which column can be searched  -->
            <el-table 
            :data="mappings.filter(data => !search || data.mapid.toLowerCase().includes(search.toLowerCase()) || data.editdate.toLowerCase().includes(search.toLowerCase()))"
            style="width: 100%"
            border
            stripe>
                <!-- bind with data -->
                <el-table-column align="center" prop="mapid" label="ID"></el-table-column>
                <el-table-column align="center" prop="username" label="Username" width="180"></el-table-column>
                <el-table-column align="center" prop="comment" label="Comment" width="180"></el-table-column>
                <el-table-column align="center" prop="editdate" label="Created At"></el-table-column>
                <el-table-column align="center" label="Action" width="360">
                    <!-- search bar -->
                    <template slot="header" slot-scope="scope">
                        <el-input v-model="search" size="mini" placeholder="Type to search"/>
                    </template>
                    <!-- operation buttons for view mapping details, download mapping result and delete mapping -->
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
    // menu active display index
    activeIndex: '2',
    // user info
    userinfo: {},
    // mapping data
    mappings: [],
    // search data
    search:''
    };
},
methods: {
    // check token and login status if token is expired or not
    // if token is expired, redirect to login page
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
    // get all mapping tasks
    // if there is no mapping task, show empty table
    // if there is mapping task, show all mapping tasks
    // if there is error, show empty table
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
    // delete mapping task
    // if delete successfully, refresh mapping task table
    // if there is error, show error message
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
    // view mapping details
    // redirect to view mapping page
    viewMapping(id){
    console.log(id);
    localStorage.setItem('mapid', id.mapid);
    localStorage.setItem('mapuserid', id.userid);
    this.$router.push("/viewmapping");
    },
    // download mapping result
    // if download successfully, download csv file
    // if there is error, show error message
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
    // handle menu select
    handleSelect(key, keyPath) {
    console.log(key, keyPath);
    if (key == 1) this.$router.push("/home");
    else if (key == 2) this.$router.push("/mapping");
    }
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
  