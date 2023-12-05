import { createRouter, createWebHistory } from 'vue-router'
import Star from '../views/Star.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import BooksView from '../views/BooksView.vue'
import BooksShow from '../views/BooksShow.vue'
import BooksReturn from '../views/BooksReturn.vue'
import BorrowingRecord from '../views/BorrowingRecord.vue'
import UserInfo from '../views/UserInfo.vue'
import test from '../views/test.vue'
import BookDetail from '../views/BookDetail.vue'
import adLogin from '../views/adLogin.vue'
import adRegister from '../views/adRegister.vue'
import adminView from '../views/adminView.vue'
import addBook from '../views/addBook.vue'
import editBook from '../views/editBook.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Star',
      component: Star
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login
    },
    {
      path: '/Register',
      name: 'Register',
      component: Register
    },
    {
      path: '/adLogin',
      name: 'adLogin',
      component: adLogin
    },
    {
      path: '/adRegister',
      name: 'adRegister',
      component: adRegister
    },
    {
      path: '/Home',
      name: 'Home',
      component: Home
    },
    {
      path: '/adminView',
      name: 'adminView',
      component: adminView,
      children: [
        {
          path: '/addBook',
          name: 'addBook',
          component: addBook,
        },
        {
          path: '/editBook',
          name: 'editBook',
          component: editBook,
        },
      ]
    },
    {
      path: '/BooksView',
      name: 'BooksView',
      component: BooksView,
      children: [
        {
          path: '/BooksShow',
          name: 'BooksShow',
          component: BooksShow,
        },
        {
          path: '/BooksReturn',
          name: 'BooksReturn',
          component: BooksReturn,
        },
        {
          path: '/BorrowingRecord',
          name: 'BorrowingRecord',
          component: BorrowingRecord,
        },
      ]
    },
    {
      path: '/UserInfo',
      name: 'UserInfo',
      component: UserInfo
    },
    {
      path: '/test',
      name: 'test',
      component: test
    },
    {
      path: '/BookDetail/:bookID',
      name: 'BookDetail',
      component: BookDetail
    },
  ]
})

export default router
