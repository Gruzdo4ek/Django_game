<script setup>
import { onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})
    

</script>
<template>

  <div class="container" >
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#"><i class="bi bi-controller"></i></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" aria-current="page" to="/">Игры</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" aria-current="page" to="/developer">Разработчики</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" aria-current="page" to="/country_developer">Страны разработчиков</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" aria-current="page" to="/genre">Жанры</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" aria-current="page" to="/platform">Платформы</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item dropdown ">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" area-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <div class=" simple-linear" >
    <div class="container"><router-view></router-view></div>
  </div>
</template>
<style lang="css" scoped>
.simple-linear {
  background: linear-gradient(rgb(255, 255, 255) , white);
}

</style>