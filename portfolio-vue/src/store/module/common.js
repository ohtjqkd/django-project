import templateSource from '../../assets/datasource.json'
const state = {
    tmpl: templateSource
}

// state: {
//     userInfo: null,
//     isLogin: false,
//     isLoginError: false
//   },
//   mutations: {
//     loginSuccess(state, payload) {
//       state.isLogin = true;
//       state.isLoginError = false;
//       state.userInfo = payload;
//     },
//     loginError(state) {
//       state.isLogin = false;
//       state.isLoginError = false;
//       state.userInfo = null;
//     },
//     logout(state) {
//       state.isLogin = false;
//       state.isLoginError = false;
//       state.userInfo = null;
//     }
//   },
//   actions: {
//     login(dispatch, loginObj) {
//       //login --> 토큰 반환
//       axios
//         .post(url, loginObj)
//         // loginObj = {email, password}
//         .then(res => {
//           // 접근 성공시, 토큰 값이 반환된다. (실제로는 토큰과 함께 유저 id를 받아온다.)
//           // 토큰을 헤더 정보에 포함시켜서 유저 정보를 요청
//           let token = res.data.token;
//           // 토큰을 로컬 스토리지에 저장
//           localStorage.setItem("access_token", token);
//           this.dispatch("getMemberInfo");
//           this.$router.push({ name: "index" });
//           console.log(res);
//         })
//         .catch(() => {
//           alert("아이디와 비밀번호를 확인하세요.");
//         })
//     },
//     logout({ commit }) {
//       commit("logout");
//       this.$router.push({ name: "index" });
//     }
//   },