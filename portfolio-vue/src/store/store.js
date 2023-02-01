import axios from 'axios'
import Vue from 'vue'
import Vuex from 'vuex'
import templateSource from '../assets/datasource.json'
// import CommonStore from './module/common'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    tmpl: templateSource,
    userInfo: null,
    isLogin: false,
    isLoginError: false,
  },
  mutations: {
    loginSuccess(state, payload) {
      state.isLogin = true;
      state.isLoginError = false;
      state.userInfo = payload;
    },
    loginError(state) {
      state.isLogin = false;
      state.isLoginError = false;
      state.userInfo = null;
    },
    logout(state) {
      state.isLogin = false;
      state.isLoginError = false;
      state.userInfo = null;
    }
  },
  actions: {
    login(dispatch, loginObj) {
      let url = "http://localhost:8000/api/rest-auth/login/";
      axios
        .post(url, loginObj)
        .then(res => {
          let token = res.data.token;
          localStorage.setItem("access_token", token);
          this.dispatch("getMemberInfo");
          this.$router.push({ name: "index"});
          console.log(res);
        })
        .catch(() => {
          alert("아이디와 비밀번호를 확인하세요.");
        })
    },
    logout({ commit }) {
      commit("logout");
      this.$router.push({ name: "index" });
    },
    changeComponent(componentName) {
      this.$contents = this.$components[componentName];
    },
    scrolling() {
      const header = document.querySelector("header");
      if (window.scrollY == 0 && header.classList.contains("background")) {
          header.classList.remove("background");
      } else if (window.scrollY != 0 && !header.classList.contains("background")) {
          header.classList.add("background");
      }
    }
  },
  mounted() {
    this.state.headerHeight = document.querySelector(".navbar").clientHeight;
  }
  // modules: {
  //   common: CommonStore
  // },
})
