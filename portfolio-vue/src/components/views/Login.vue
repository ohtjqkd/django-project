<template>
    <v-layout class="formContainer">
        <v-form ref="form" class="login-box">
            <p>아이디</p>
            <input type="text" v-model="username" name="username" label="ID를 입력하세요" />
            <p>비밀번호</p>
            <input type="password" v-model="password" name="userpassword" label="비밀번호를 입력하세요" />
        </v-form>
        <div class="login-btn">
            <input type="submit" class="button" name="submit" @click="login({username, password})" value="로그인" />
        </div>
    </v-layout>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
    data() {
        return {
            username: null,
            password: null
        };
    },
    computed: {
        ...mapState(["isLogin", "isLoginError"])
    },
    methods: {
        ...mapActions(["login"])
    }
}

</script>