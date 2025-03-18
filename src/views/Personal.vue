<template>
  <div>
    <div class="PersonTop">
      <div class="PersonTop_img">
        <img v-image-preview :src="avatar" />
      </div>
      <div class="PersonTop_text">
        <div class="user_text">
          <div class="user_name">
            <span> {{ nickname }} </span>
          </div>
          <div class="user-v" v-if="v === 3">
            <img :src="avatar" class="user-v-img" />
            <span class="user-v-font">优质媒体作者</span>
          </div>
          <div class="user_qianming">
            <span> {{ design }}</span>
          </div>
          <div class="user_anniu">
            <el-button class="el-icon-edit" type="primary" size="medium" plain @click="edit">编辑</el-button>
            <!-- <el-button @click="follow" type="primary" size="medium" icon="el-icon-check" v-text="1
              ? '已关注'
              : '关注'
              "></el-button> -->
          </div>
        </div>
        <div class="user_num">
          <div style="cursor: pointer" @click="myfan">
            <div class="num_number">{{ fanCounts }}</div>
            <span class="num_text">粉丝</span>
          </div>
          <div style="cursor: pointer" @click="myfollow">
            <div class="num_number">{{ followCounts }}</div>
            <span class="num_text">关注</span>
          </div>
          <div>
            <span class="num_text">正确问题</span>
            <div class="num_number">{{ goodCounts }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="person_body">
      <div class="person_body_left">
        <el-card class="box-card" :body-style="{ padding: '0px' }">
          <div slot="header" class="clearfix">
            <span class="person_body_list" style="border-bottom: none">个人中心</span>
          </div>
          <!-- <div
            class="person_body_list"
            v-for="(item, index) in person_body_list"
            :key="index"
          >
            <router-link :to="{ name: item.name, params: item.params }">{{
              item.label
            }}</router-link>
          </div> -->
          <el-menu router active-text-color="#00c3ff" class="el-menu-vertical-demo">
            <el-menu-item index="info">
              <i class="el-icon-user"></i>
              <span slot="title">个人简介</span>
            </el-menu-item>
            <el-menu-item index="myarticle">
              <i class="el-icon-edit-outline"></i>
              <span slot="title">发帖</span>
            </el-menu-item>
            <el-menu-item index="mycollect">
              <i class="el-icon-document"></i>
              <span slot="title">收藏</span>
            </el-menu-item>
            <el-menu-item index="myfan">
              <i class="el-icon-tableware"></i>
              <span slot="title">粉丝</span>
            </el-menu-item>
            <el-menu-item index="myfollow">
              <i class="el-icon-circle-plus-outline"></i>
              <span slot="title">关注</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </div>
      <div class="person_body_right">
        <Info />
      </div>
    </div>
    <personal-dia ref="personalDiaRef" @flesh="reload" />
  </div>
</template>

<script>
// import { userInfo } from "@/api/user";
// import {
//   myFollow,
//   addFollow,
//   deleteFollow,
//   followAndFanCount,
// } from "@/api/follow.js";
// import { mygoodCount } from "@/api/good";
import multiavatar from '@multiavatar/multiavatar'; // 引入 multiavatar
import PersonalDia from "./PersonalDia.vue";
import Info from "./Info.vue"
import { userState, setUser } from '@/store/userStore'


export default {
  components: { PersonalDia, Info },
  name: "Personal",
  inject: ["reload"],
  data() {
    return {
      avatar: "",
      nickname: "",
      v: 1,
      design: "",
      followCounts: "",
      fanCounts: "",
      goodCounts: "",
      isfollow: true,
      followData: {
        fanId: "",
        followId: "",
      },
      isfollowid: [],
      // person_body_list: [
      //   {
      //       //     label: "个人简介",
      //       //     name: "info",
      //       //     params: { id: this.$route.params.id },
      //       //   },
      //       //   {
      //       //     label: "发帖",
      //       //     name: "myarticle",
      //       //     params: { id: this.$route.params.id },
      //       //   },
      //       //   {
      //       //     label: "收藏",
      //       //     name: "mycollect",
      //       //     params: { id: this.$route.params.id },
      //       //   },
      //       //   {
      //       //     label: "粉丝",
      //       //     name: "myfan",
      //       //     params: { id: this.$route.params.id },
      //       //   },
      //       //   {
      //       //     label: "关注",
      //       //     name: "myfollow",
      //       //     params: { id: this.$route.params.id },
      //       //   },
      //       // ],
    };
  },
  mounted() {
    this.load();
    this.getRandomheader()
  },
  //   watch: {
  //     $route(to, from) {
  //       if (to.path == `/newsuser/personal/${this.$store.state.id}`) {
  //         // this.load();
  //         // this.person_body_list.forEach((res) => {
  //         //   res.params.id = this.$store.state.id;
  //         // });
  //         this.reload();
  //       } else if (to.path == `/newsuser/personal/${this.$route.params.id}`) {
  //         this.reload();
  //       }
  //     },
  //   },
  methods: {
    load() {
      //       // this.$store //必须使用此种方法，否则response拦截器会拦截
      //       //   .dispatch("getUserInfo", this.$store.state.token) //利用vuex
      //       //   .then((res) => {})
      //       //   .catch((error) => {
      //       //     console.log(error);
      //       //   });
      //       userInfo(this.$route.params.id)
      //         .then((res) => {
      //           console.log(res);
      //           this.avatar = res.data.avatar;
      //           this.nickname = res.data.nickname;
      //           this.v = res.data.v;
      //           this.design = res.data.design;
      //         })
      //         .catch((err) => {
      //           console.log(err);
      //         });
      this.goodCounts = userState.user.correct_problems
      this.goodCounts = userState.user.correct_problems
      this.createDate = new Date(userState.user.created_at).toISOString().split('T')[0];
      this.email = userState.user.email;
      this.sex = userState.user.gender ? userState.user.gender : "未完善";
      this.age = userState.user.grade ? userState.user.grade : "未完善";
      this.design = userState.user.remarks ? userState.user.remarks : "未完善";
      this.account = userState.user.username;
      this.nickname = userState.user.username;

      //       myFollow(this.$store.state.id)
      //         .then((res) => {
      //           res.data.forEach((res) => {
      //             this.isfollowid.push(res.id);
      //           });
      //         })
      //         .catch((err) => {
      //           console.log(err);
      //         });

      //       followAndFanCount(this.$route.params.id)
      //         .then((res) => {
      //           this.followCounts = res.data.followCounts;
      //           this.fanCounts = res.data.fanCounts;
      //         })
      //         .catch((err) => {
      //           console.log(err);
      //         });

      //       mygoodCount(this.$route.params.id)
      //         .then((res) => {
      //         })
      //         .catch((err) => {
      //           console.log(err);
      //         });
      //     },
      //     myfan() {
      //       this.$router.push({
      //         path: `/newsuser/personal/myfan/${this.$route.params.id}`,
      //       });
      //     },
      //     myfollow() {
      //       this.$router.push({
      //         path: `/newsuser/personal/myfollow/${this.$route.params.id}`,
      //       });
      //     },
      //     follow() {
      //       if (!this.$store.state.id) {
      //         this.$message({
      //           showClose: true,
      //           message: "请登录后再进行操作哦",
      //           type: "warning",
      //         });
      //       } else {
      //         this.followData.followId = this.$route.params.id;
      //         this.followData.fanId = this.$store.state.id;
      //         if (this.isfollowid.indexOf(this.followData.followId) > -1) {
      //           this.isfollow = true;
      //         } else {
      //           this.isfollow = false;
      //         }
      //         if (this.isfollow) {
      //           deleteFollow(this.followData)
      //             .then((res) => {
      //               this.isfollow = false;
      //               this.$message({
      //                 showClose: true,
      //                 message: "已取消关注",
      //                 type: "success",
      //               });
      //               this.reload();
      //             })
      //             .catch((err) => {
      //               console.log(err);
      //             });
      //         } else if (!this.isfollow) {
      //           addFollow(this.followData)
      //             .then((res) => {
      //               this.isfollow = true;
      //               this.$message({
      //                 showClose: true,
      //                 message: "已成功关注",
      //                 type: "success",
      //               });
      //               this.reload();
      //             })
      //             .catch((err) => {
      //               console.log(err);
      //             });
      //         }
      //       }
      //     },
    },
    edit() {
      this.$refs.personalDiaRef.open();    },
    getRandomheader() {
      const svg = multiavatar(userState.user.user_id); // 使用 multiavatar 生成 SVG 图像
      this.avatar = `data:image/svg+xml;base64,${btoa(svg)}`;
    },
  },
};
</script>

<style scoped>
/* 新增现代化配色方案 */
:root {
  --primary-color: #4361ee;
  /* 主色调调整为更活力的蓝色 */
  --secondary-color: #3f37c9;
  --text-dark: #2d3748;
  --text-medium: #4a5568;
  --text-light: #718096;
  --background-light: #f8f9fa;
}

.PersonTop {
  width: 90%;
  max-width: 1200px;
  height: auto;
  padding: 2rem;
  margin: 2rem auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 2rem;
  transition: all 0.3s ease;
}

/* .PersonTop:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
} */

.PersonTop_img {
  width: 120px;
  height: 120px;
  flex-shrink: 0;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--background-light);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  /* transition: transform 0.3s ease; */
}

/* .PersonTop_img:hover {
  transform: scale(1.05);
} */

.PersonTop_text {
  height: 120px;
  width: 880px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.user_text {
  margin-bottom: 1rem;
}

.user_name {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-dark);
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: #2d3748;
}

.user-v {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  padding: 0.2rem 0.8rem;
  border-radius: 20px;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.user-v-font {
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
}

.user_qianming {
  color: var(--text-light);
  font-size: 0.95rem;
  margin: 0.5rem 0;
  line-height: 1.4;
}

.user_anniu {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.user_anniu .el-button {
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.user_anniu .el-button--primary {
  background: linear-gradient(135deg, #00c3ff 0%, #0066ff 100%);
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  color: #f8f9fa;
}

.user_anniu .el-button--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(67, 97, 238, 0.3);
}

.user_num {
  display: flex;

  gap: 3rem;
  padding: 1rem 0;
}

.user_num>div {
  text-align: center;
  padding: 0 1rem;
}

.user_num>div:not(:last-child)::after {
  content: "";
  position: absolute;
  right: -1.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 40%;
  background: #e2e8f0;
}

.num_number {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 0.2rem;
}

.num_text {
  color: var(--text-light);
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

/* 导航菜单优化 */
.person_body {
  width: 90%;
  max-width: 1200px;
  margin: 2rem auto;
  display: flex;
  gap: 2rem;
}

.person_body_left {
  width: 280px;
  flex-shrink: 0;
}

.box-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: none;
}

.el-menu {
  border-right: none !important;
  padding: 1rem 0;
}

.el-menu-item {
  height: 48px;
  line-height: 48px;
  margin: 0.4rem 0;
  border-radius: 8px;
  transition: all 0.2s ease;
  color: var(--text-medium);
}

.el-menu-item:hover {
  background: var(--background-light);
  transform: translateX(4px);
}

.el-menu-item.is-active {
  color: var(--primary-color) !important;
  background: rgba(67, 97, 238, 0.1);
  font-weight: 500;
}

.el-menu-item i {
  margin-right: 1rem;
  font-size: 1.1rem;
}

/* 右侧内容区域 */
.person_body_right {
  flex: 1;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .PersonTop {
    flex-direction: row;
    align-items: center;
    text-align: center;
  }

  .user_anniu {
    justify-content: center;
  }

  .person_body {
    flex-direction: column;
  }

  .person_body_left {
    width: 100%;
  }

  .user_num {
    justify-content: center;
    gap: 2rem;
  }
}
</style>
