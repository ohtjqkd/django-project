<template>
    <div>
        <section id="top">
            <div class="vert-middle">
                <h1>- 오준석 -</h1>
                <h1>웹 개발자 포트폴리오</h1>
                <p>계속 앞으로 나아가는 개발자입니다.</p>
                <p>모든 일을 [즐겁게, 잘] 하자를 추구합니다.</p>
            </div>
        </section>
        <section id="aboutme">
            <h1>
                About Me
            </h1>
            <div class="aboutme-wrapper">
                <div v-for="info in contents.aboutme" v-bind:key="info.label" class="info-wrapper">
                    <div class="info-wrapper ico"><img v-bind:src="info.ico" /></div>
                    <div class="info-wrapper field">
                        <div class="info-wrapper field label"><b>{{info.label}}</b></div>
                        <div class="info-wrapper field value">{{info.desc}}</div>
                    </div>
                </div>
            </div>
        </section>
        <section id="skills">
            <h1>
                Skills
            </h1>
            <div class="skill-wrapper">
                <div class="domain round" v-for="set in contents.skill_set" v-bind:key="set.domain">
                    <h2 class="domain_name">
                        {{set.domain}}
                    </h2>
                        <i v-for="i in set.skills" v-bind:key="i" v-bind:class="i"></i>
                </div>
            </div>
        </section>
        <section id="projects">
            <h1>
                Projects
            </h1>
            <!-- {% for project in projects %} -->
                <article class="project round" v-for="project in contents.projects" v-bind:key="project.name">
                    <h2>
                    {{project.name}}
                    </h2>
                    <section class="projects image-field">
                        <!-- <swiper :slides-per-view="3" :space-between="50" @swiper="onSwiper" @slideChange="onSlideChange">
                            <swiper-slide v-for="src in project.images" v-bind:key="src"><img src:src></swiper-slide>
                        </swiper> -->
                        <div class="swiper">
                            <div class="swiper-wrapper">
                                <div class="swiper-slide" v-for="image in project.images" v-bind:key="image.src">
                                    <!-- <img :src="require(image)"> -->
                                </div>
                            </div>
                            <div class="swiper-pagination"></div>
                        </div>
                    </section>
                    <!-- <section class="projects desc-field"> -->
                        <!-- <v-html:tag="desc.tag" v-for="desc in project.description" :key="project.desc"> -->
                            <!-- <{{desc.tag}}>{{desc.text}}</{{desc.tag}}> -->
                        <!-- <br>
                        <div class="projects info-field">
                                <div class="projects info-field info">
                                    <div class="projects info-field info label">
                                        {{label}}
                                    </div>
                                    <div class="projects info-field info value">
                                        {{value}}
                                    </div>
                                </div>
                        </div>
                    </section> -->
                </article>
        </section>
        <!-- <section id="experiences"> -->
        <!-- </section> -->
        <!-- <a href="https://icons8.com/icon/qULYrKvr-AFH/django">Django icon by Icons8</a>
        <a href="https://icons8.com/icon/t2x6DtCn5Zzx/nginx">Nginx icon by Icons8</a>
        <a href="https://icons8.com/icon/11625/mysql">MySQL icon by Icons8</a>
        <a href="https://icons8.com/icon/bpip0gGiBLT1/opencv">OpenCV icon by Icons8</a>
        <script src="{% static 'portfolio/js/portfolio.js' %}"></script> -->
    </div>
</template>

<script>
import { Swiper, Navigation, Pagination, /*Scrollbar, A11y*/ } from 'swiper';
// import SwiperSlide from 'swiper'
import 'swiper/swiper.scss';

Swiper.use([Navigation, Pagination])

export default {
    data() {
        return {
            contents: this.$store.state.tmpl.contents
        }
    },
    // components: {
    //     Swiper,
    //     SwiperSlide,
    // },
    mounted() {
        new Swiper('.swiper-container', {
            loop: true,
            pagination: {
                el: '.swiper-pagination',
            }
        })
    },
    // setup() {
    //     const onSwiper = (swiper) => {
    //         console.log(swiper);
    //     };
    //     const onSlideChange = () => {
    //         console.log('slide change');
    //     };
    //     return {
    //         onSwiper,
    //         onSlideChange,
    //         modules: [Navigation, Pagination, Scrollbar, A11y],
    //     }
    // },
    props:["propsdata"],
    methods: {
        loadImg: function(src) {
            console.log(typeof(src));
            console.log(src);
            return require(''+src);
        }
        // sendForm: function() {
        //     axios({
        //         method: "POST",
        //         url: url,
        //         data: this.data,
        //     })
        //         .then((response) => {
        //             this.userList = response.data;
        //         })
        //         .catch((error) => {
        //             console.log("Failed to get userList", error.response);
        //         });
        // },
        // clearForm: function() {
        //     (this.data.username = ""), (this.data.age = ""), (this.data.city = "");
        // },
    },
};
</script>

<style>

</style>