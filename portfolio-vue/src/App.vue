<template>
    <div id="app">
        <div id="header">
            <Header />
        </div>
        <div id="container" class="content">
            <router-view></router-view>
        </div>
        <div id="footer">
            <Footer />
        </div>
    </div>
</template>

<script>
import Header from "@/components/layout/Header.vue"
import Footer from "@/components/layout/Footer.vue"

// import axios from "axios"

export default {
    data: function() {
        return {
            userList: [],
        };
    },
    components: {
        Header,
        Footer,
    },
    // mounted() { // DOM 객체가 생성된 후 DRF server에서 데이터를 가져와 저장
    //     axios({
    //         method: "GET",
    //         url: url,
    //     }).then((result) => {
    //         this.userList = result.data; 
    //     }).catch((err) => {
    //         console.log("Failed", err);
    //     });
    // },
    methods: { // CRUD 로직
        getUserList: function() {},
        updateUserList: function() {},
        deleteUserList: function() {},
    }
};
</script>

<style></style>
