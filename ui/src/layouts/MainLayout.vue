<template>
  <q-layout>
    <q-header style="background-color: rgba(0, 0, 0, 0)">
      <!--ヘッダー-->

      <div
        style="
          height: 60px;
          padding-top: 16px;
          padding-left: 24px;
          display: flex;
          justify-content: space-between;
        "
      >
        <!--ヘッダーの左側-->
        <div
          style="
            font-size: 18px;
            width: 200px;
            color: rgb(51, 51, 51);
            background-color: rgb(234, 246, 251);
            border-radius: 0px 10px 10px 0px;
            position: relative;
            left: -24px;
          "
          class="fadeDown"
          v-if="!menuView"
        >
          <div
            style="padding-left: 8px; padding-top: 8px; cursor: pointer"
            @click="router.push('/')"
          >
            ホロ餅
          </div>
        </div>

        <!--ヘッダーの右側(PC用)-->
        <div
          class="nav-top fadeDown"
          style="padding-right: 100px; background-color: rgb(234, 246, 251)"
        >
          <div class="nav-child">
            <span @click.prevent="pageClick('/', 0)">top</span>
          </div>
          <div class="nav-child">
            <div @mouseover="headerOpen(1)" @click="headerOpen(1)">
              <q-icon name="expand_more" />content
            </div>
          </div>
        </div>
      </div>
      <div class="nav-top" style="width: 100%; max-width: 100%">
        <div style="width: 200px"></div>
        <div class="nav-child">
          <div
            class="balloon1-top fadeDown"
            :class="{ 'hover-page': head.id == 1, 'hover-other': head.id != 1 }"
            style="cursor: default"
            v-if="head.id > 0"
          >
            <div>
              <div class="row">
                <div
                  class="col"
                  v-for="page in nowPage(head.id)"
                  :key="page.id"
                  style="color: rgb(51, 51, 51); font-size: 16px"
                >
                  <div class="q-mb-sm row">
                    <div>{{ page.title }}</div>
                    <div class="q-ml-xs" style="position: relative; top: 2px; left: 2px">
                      <img
                        v-if="page.img"
                        :src="page.img"
                        style="height: 20px; width: 20px; object-fit: contain"
                      />
                    </div>
                  </div>

                  <div
                    v-for="item in nowPageList(page.id, head.id)"
                    :key="item.title"
                    style="color: rgb(51, 51, 51)"
                  >
                    <a
                      class="nav-content q-pb-xs row"
                      @click.prevent="pageClick(item.url, head.id)"
                    >
                      <div>{{ item.title }}</div>
                      <div class="q-ml-xs">
                        <img
                          v-if="item.img"
                          :src="item.img"
                          style="height: 20px; width: 20px; object-fit: contain"
                        />
                      </div>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!--ヘッダー右側(スマホ用)-->
      <div
        class="top-menu-button nav-top-mini"
        @click="menuView = !menuView"
        :class="{ active: menuView }"
      >
        <span> </span><span> </span><span></span>
      </div>
    </q-header>

    <nav id="g-nav" :class="{ panelactive: menuView }">
      <div id="g-nav-list">
        <div class="g-nav-main">
          <div v-for="headId in [1, 2]" :key="headId">
            <div
              class="g-nav-item"
              v-for="page in nowPage(headId)"
              :key="page.id"
              style="color: rgb(51, 51, 51); font-size: 16px"
            >
              <div class="q-mb-sm row q-mt-md">
                <div>{{ page.title }}</div>
                <div class="q-ml-xs" style="position: relative; top: 2px; left: 2px">
                  <img
                    v-if="page.img"
                    :src="page.img"
                    style="height: 20px; width: 20px; object-fit: contain"
                  />
                </div>
              </div>

              <div
                v-for="item in nowPageList(page.id, headId)"
                :key="item.title"
                style="color: rgb(51, 51, 51)"
              >
                <a class="nav-content q-pb-xs row" @click.prevent="pageClick(item.url, headId)">
                  <div>{{ item.title }}</div>
                  <div class="q-ml-xs">
                    <img
                      v-if="item.img"
                      :src="item.img"
                      style="height: 20px; width: 20px; object-fit: contain"
                    />
                  </div>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <!--ページ-->
    <q-page-container style="position: relative" @click="headerClose()">
      <router-view class="q-pa-md" />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import type { Router } from 'vue-router';
import { useRouter } from 'vue-router';
//import { createPinia, setActivePinia } from 'pinia'

export default defineComponent({
  name: 'MainLayout',

  setup() {
    const router = useRouter();
    const opened = ref(false);
    const menuView = ref(false);
    //setActivePinia(createPinia())
    const leftDrawerOpen = computed(() => opened.value);

    const head = ref({
      id: 0,
      display: false,
    } as head);

    const headerOpen = function (id: number) {
      head.value.id = id;
      head.value.display = true;
    };

    const headerClose = function () {
      head.value.id = 0;
      head.value.display = false;
      menuView.value = false;
    };

    const headerClick = function (id: number) {
      if (head.value.id == 0 || id != 0) {
        headerOpen(id);
      } else {
        headerClose();
      }
    };

    /*page */
    const { callPageList, pages, nowPage, nowPageList, openLink } = usePage(router);

    const otherPageClick = function (url: string) {
      window.open(url);
      headerClose();
    };

    const pageClick = function (url: string, headId: number) {
      openLink(url, headId);
      headerClose();
    };

    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        opened.value = !opened.value;
      },
      router,
      head,
      headerOpen,
      headerClose,
      headerClick,
      callPageList,
      pages,
      otherPageClick,
      menuView,
      nowPage,
      nowPageList,
      pageClick,
    };
  },
});
interface headItem {
  title: string;
  id: number;
  img?: string;
  icon?: string;
}
interface head {
  id: number;
  display: boolean;
}
interface PageState {
  title: string;
  url: string;
  img?: string;
}

/*page function */
function usePage(router: Router) {
  const fanartPages = ref([
    {
      title: 'twitter',
      url: '/twitter',
    },
  ] as PageState[]);

  const moviePages = ref([] as PageState[]);

  function callPageList(no: number) {
    if (no == 1) return fanartPages.value;
    if (no == 2) return moviePages.value;
    return [] as PageState[];
  }

  const pages = ref([
    {
      id: 1,
      title: 'ファンアート',
      img: 'https://img.icons8.com/ios/250/000000/picture.png',
    },
    {
      id: 2,
      title: 'YouTube',
      img: 'https://img.icons8.com/ios/250/000000/tv-show.png',
    },
  ] as headItem[]);

  function nowPage(id: number) {
    if (id == 1) {
      return pages.value;
    }
    return [];
  }

  function nowPageList(id: number, headId: number) {
    if (headId == 1) {
      return callPageList(id);
    }
    return [];
  }

  function openLink(url: string, headId: number) {
    if (headId == 2) {
      window.open(url, '_blank');
    } else {
      void router.push(url);
    }
  }

  return {
    pages,
    callPageList,
    nowPage,
    nowPageList,
    openLink,
  };
}
</script>
<style>
.menu-icon-image {
  width: 52px;
}
body {
  background-image: url('../assets/bg.jpg');
  color: #063f5c;
  font-family: 'Noto Sans JP', sans-serif;
}
/*navigation */
.nav-top {
  justify-content: flex-end;
  display: flex;
  padding-top: 10px;
  padding-right: 20px;
  padding-left: 10px;
  width: calc(100% - 200px);
  max-width: 450px;
  height: 100%;
  border-radius: 10px 0 0 10px;
}
@media (max-width: 930px) {
  .nav-top {
    display: none;
  }
}
@media (max-width: 930px) {
  /*========= ボタンのためのCSS ===============*/
  .top-menu-button {
    position: fixed;
    z-index: 9999; /*ボタンを最前面に*/
    top: 10px;
    right: 10px;
    cursor: pointer;
    width: 50px;
    height: 50px;
  }

  /*×に変化*/
  .top-menu-button span {
    display: inline-block;
    transition: all 0.4s;
    position: absolute;
    left: 14px;
    height: 3px;
    border-radius: 2px;
    background-color: #666;
    width: 45%;
  }

  .top-menu-button span:nth-of-type(1) {
    top: 15px;
  }

  .top-menu-button span:nth-of-type(2) {
    top: 23px;
  }

  .top-menu-button span:nth-of-type(3) {
    top: 31px;
  }

  .top-menu-button.active span:nth-of-type(1) {
    top: 18px;
    left: 18px;
    transform: translateY(6px) rotate(-45deg);
    width: 30%;
  }

  .top-menu-button.active span:nth-of-type(2) {
    opacity: 0;
  }

  .top-menu-button.active span:nth-of-type(3) {
    top: 30px;
    left: 18px;
    transform: translateY(-6px) rotate(45deg);
    width: 30%;
  }
}
/*========= ナビゲーションのためのCSS ===============*/

#g-nav {
  /*position:fixed;にし、z-indexの数値を大きくして前面へ*/
  position: fixed;
  z-index: 2;
  /*ナビのスタート位置と形状*/
  top: -120%;
  left: 0;
  width: 100%;
  height: 100vh; /*ナビの高さ*/
  background: white;
  /*動き*/
  transition: all 0.6s;
  overflow-y: scroll;
}

/*アクティブクラスがついたら位置を0に*/
#g-nav.panelactive {
  top: 0;
}

/*ナビゲーションの縦スクロール*/
#g-nav.panelactive #g-nav-list {
  /*ナビの数が増えた場合縦スクロール*/
  margin-top: 50px;
  position: fixed;
  width: 100%;
  height: calc(100vh - 60px); /*表示する高さ*/
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
}

/*ナビゲーション*/
#g-nav .g-nav-main {
  position: absolute;
  z-index: 999;
  /*ナビゲーション天地中央揃え*/
  top: 60px;
  left: 50%;
  transform: translate(-50%, -60px);
}

/*リストのレイアウト設定*/
#g-nav .g-nav-item {
  list-style: none;
  text-align: center;
  z-index: 10;
}

#g-nav .g-nav-item a {
  color: rgb(51, 51, 51);
  text-decoration: none;
  padding: 10px;
  display: block;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.nav-child {
  color: #333;
  text-decoration: none;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1.85;
  transition: color 0.3s ease;
  padding-right: 32px;
  height: 100%;
  width: 120px;
  position: relative;
  z-index: 2;
}
.nav-child:hover {
  color: rgb(178, 222, 224);
}
.nav-child-select {
  background-color: rgba(202, 220, 175, 1);
  color: rgb(127, 109, 98);
  border-bottom: 1.5px dashed rgba(51, 51, 51, 0.2); /* 線の太さ、スタイル、色を指定 */
}
.nav-child-select:hover {
  background-color: rgba(182, 200, 155, 1);
}
.nav-child-page {
  height: 50px;
  width: 160px;
  cursor: pointer;
}
/* 右から */

.fadeRight {
  animation-name: fadeRightAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  opacity: 0;
  z-index: 2;
}

@keyframes fadeRightAnime {
  from {
    opacity: 0;
    transform: translateX(100px);
    z-index: 2;
  }

  to {
    opacity: 1;
    transform: translateX(0);
    z-index: 2;
  }
}
/* 上から */

.fadeDown {
  animation-name: fadeDownAnime;
  animation-duration: 0.5s;
  animation-fill-mode: forwards;
  opacity: 0;
}

@keyframes fadeDownAnime {
  from {
    opacity: 0;
    transform: translateY(-100px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
/*
  トップスクロール
*/
.scroll-to-top {
  border: none;
  background-color: rgba(0, 0, 0, 0);
  position: fixed;
  bottom: 10px;
  right: 10px;
  padding: 5px 10px;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.3s ease;
}
@media (max-width: 800px) {
  .scroll-to-top {
    display: none;
  }
}

.scroll-to-top:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
.balloon1-top {
  position: absolute;
  left: -310px;
  margin: 1.5em 0;
  padding: 10px 14px;
  width: 400px;
  color: #555;
  font-size: 16px;
  background: rgb(234, 246, 251);
  border-radius: 20px;
  box-shadow: 0 0px 10px 0 rgba(0, 0, 0, 0.1);
}

.balloon1-top:before {
  content: '';
  position: absolute;
  top: -30px;
  margin-left: 130px;
  border: 15px solid transparent;
  border-bottom: 15px solid rgb(234, 246, 251);
}

.balloon1-top p {
  margin: 0;
  padding: 0;
}
.nav-content {
  cursor: pointer;
  font-size: 14px;
}
.nav-content:hover {
  transition: 0.3s;
  color: rgb(178, 222, 224);
}

.hover-page::before {
  left: 30%;
}

.hover-other::before {
  left: 50%;
}
</style>
