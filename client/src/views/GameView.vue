<script setup>
import axios from 'axios';
import { storeToRefs } from 'pinia';
import _ from 'lodash';
import { computed, ref, onBeforeMount, watch } from 'vue'
import useUserProfileStore from '@/stores/userProfileStore';
import { Modal } from 'bootstrap';

const userProfileStore = useUserProfileStore();
const {
  isAuthorized,
  isSuperUser,
  username
} = storeToRefs(userProfileStore)

const users = ref([]);
const games = ref([]);
const loading = ref(false);
const gameToAdd = ref({});
const gameToEdit = ref({});
const developer = ref([]);
const genre = ref([]);
const platform = ref([]);
const delevoperById = computed(() => {
  return _.keyBy(developer.value, x => x.id)
})
const genreById = computed(() => {
  return _.keyBy(genre.value, x => x.id)
})
const platformById = computed(() => {
  return _.keyBy(platform.value, x => x.id)
})
const gamesPictureRef = ref();
const gamesAddImageUrl = ref();
const selectedImageUrl = ref('');
const editGamePictureRef = ref();
const gamesEditImageUrl = ref();
const selectedUserId = ref()
const alert403 = ref(false);
const gameStats = ref({});
const selectedGenreId = ref()
const selectedPlatformId = ref()
const otpCode = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const otpModalVisible = ref(false);
const editModalVisible = ref(false);
const modalElement = ref(null);
const isOtpVerified = ref(false); // Состояние для проверки OTP
const sortOrder = ref('asc');

const sortedGames = computed(() => {
  return [...games.value].sort((a, b) => {
    if (sortOrder.value === 'asc') {
      return a.name.localeCompare(b.name); // Сортировка от A до Z
    } else {
      return b.name.localeCompare(a.name); // Сортировка от Z до A
    }
  });
});
const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
};

watch(editModalVisible, (newValue) => {
  if (newValue && modalElement.value) {
    const modalInstance = new Modal(modalElement.value);
    modalInstance.show();
  }
});

const verifyOtp = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const response = await axios.post('/api/user-profile/otp-login/', { otp_key: otpCode.value });

    if (response.data.success) {
      successMessage.value = 'OTP код успешно проверен!';
      otpModalVisible.value = false; // Закрываем окно OTP
      console.log('editModalVisible до:', editModalVisible.value);
      editModalVisible.value = true;
      console.log('editModalVisible после:', editModalVisible.value);
      isOtpVerified.value = true;
    } else {
      errorMessage.value = 'Неверный OTP код, попробуйте снова.';
    }
  } catch (error) {
    errorMessage.value = 'Произошла ошибка при проверке OTP. Попробуйте снова позже.';
  } finally {
    isLoading.value = false;
  }
};

async function exportExcel() {
  try {
    const response = await axios.get("/api/games/export-excel/", {
      responseType: 'blob'
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'games.xlsx');
    document.body.appendChild(link);
    link.click();
  } catch (error) {
    console.error("Ошибка при экспорте в Excel:", error);
  }
}

async function fetchStats() {
  try {
    const response = await axios.get("/api/games/stats/");
    gameStats.value = response.data;
    console.log(gameStats.value); // Verify the data
  } catch (error) {
    console.error("Error fetching statistics:", error);
  }
}

async function fetchUsers() {
  const r = await axios.get("/api/user/");
  users.value = r.data
  console.log(users.value)
}

async function fetchGenre() {
  const r = await axios.get("/api/genre/");
  console.log(r.data)
  genre.value = r.data;
}

async function fetchPlatform() {
  const r = await axios.get("/api/platform/");
  console.log(r.data)
  platform.value = r.data;
}

async function fetchDeveloper() {
  const r = await axios.get("/api/developer/");
  console.log(r.data)
  developer.value = r.data;
}

async function fetchGames(selectedUserId, selectedGenreId, selectedPlatformId) {
  loading.value = true;
  const r = await axios.get("/api/games/");
  let filterData = r.data

  if (selectedUserId.value != null) {
    filterData = filterData.filter(it => it.user === selectedUserId.value)
  }
  if (selectedGenreId.value != null) {
    filterData = filterData.filter(it => it.genre_fk === selectedGenreId.value)
  }
  if (selectedPlatformId.value != null) {
    filterData = filterData.filter(it => it.platform_fk === selectedPlatformId.value)
  }

  games.value = filterData

  console.log(selectedUserId.value)
  console.log(selectedGenreId.value)
  console.log(selectedPlatformId.value)
  console.log(games.value)
}

async function handleGenreChange() {
  await fetchGames(selectedUserId, selectedGenreId, selectedPlatformId)
}

async function handlePlatformChange() {
  await fetchGames(selectedUserId, selectedGenreId, selectedPlatformId)
}

async function onGameAdd() {
  try {
    const formData = new FormData();
    if (gamesPictureRef.value.files[0]) {
      formData.append('picture', gamesPictureRef.value.files[0]);
    } else {
      console.error("No picture selected");
    }

    formData.set('name', gameToAdd.value.name);
    formData.set('developer_fk', gameToAdd.value.developer_fk); // Исправлено
    formData.set('genre_fk', gameToAdd.value.genre_fk);         // Исправлено
    formData.set('platform_fk', gameToAdd.value.platform_fk);   // Исправлено

    await axios.post("/api/games/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    await fetchGames(selectedUserId, selectedGenreId, selectedPlatformId);
  } catch (error) {
    if (error.response && error.response.status === 403) {
      alert403.value = true
    }
  }

  gameToAdd.value = {}
  gamesAddImageUrl.value = ''
  gamesPictureRef.value.value = ''
}

async function gamesAddPictureChange() {
  gamesAddImageUrl.value = URL.createObjectURL(gamesPictureRef.value.files[0])
}

async function gamesEditPictureChange() {
  if (editGamePictureRef.value && editGamePictureRef.value.files && editGamePictureRef.value.files[0]) {
    gamesEditImageUrl.value = URL.createObjectURL(editGamePictureRef.value.files[0]);
  } else {
    console.error("No picture file selected.");
  }
}
async function onRemoveClick(game) {
  console.log(game);
  if (isOtpVerified.value) {
    await axios.delete(`/api/games/${game.id}/`);
    await fetchGames(selectedUserId, selectedGenreId, selectedPlatformId);
  } else {
    otpModalVisible.value = true;
  }
}

async function onEditClick(game) {
  gameToEdit.value = { ...game };
  gamesEditImageUrl.value = game.picture || ''
  if (isOtpVerified.value) {
    // Если OTP уже проверен, сразу показываем окно редактирования
    editModalVisible.value = true;
  } else {
    // В противном случае показываем модалку OTP
    otpModalVisible.value = true;
  }
}

async function openImageModal(imageUrl) {
  selectedImageUrl.value = imageUrl;
  const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
  imageModal.show();
}
function closeModal() {
  editModalVisible.value = false; // Скрыть модальное окно
}

async function onUpdateGame() {
  const formData = new FormData();
  formData.set('name', gameToEdit.value.name);
  formData.set('developer_fk', gameToEdit.value.developer_fk);
  formData.set('genre_fk', gameToEdit.value.genre_fk);
  formData.set('platform_fk', gameToEdit.value.platform_fk);

  if (editGamePictureRef.value && editGamePictureRef.value.files[0]) {
    formData.append('picture', editGamePictureRef.value.files[0]);
  }

  try {
    await axios.put(`/api/games/${gameToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    await fetchGames(selectedUserId, selectedGenreId, selectedPlatformId);
    closeModal();
  } catch (error) {
    console.error("Error updating game:", error.response.data);
  }
}
async function handleUserChange() {
  await fetchGames(selectedUserId, selectedGenreId, selectedPlatformId)
}

onBeforeMount(async () => {
  await fetchStats();
  await fetchGames(selectedUserId, selectedGenreId, selectedPlatformId);
  await fetchDeveloper();
  await fetchGenre();
  await fetchPlatform();
})

watch(isSuperUser, () => {
  if (isSuperUser.value) {
    console.log(isSuperUser.value)
    fetchUsers()
  }
}, {
  immediate: true
})

</script>

<template>
  <div class="container-fluid">
    <div class="alert alert-cst" role="alert" v-if="isAuthorized === false">
      Вы должны быть авторизованы для работы со страницей.
    </div>
    <div class="alert alert-cst-403" role="alert" v-if="alert403 === true">
      Вы должны быть авторизованы для выполнения этого действия.
    </div>
    <form @submit.prevent.stop="onGameAdd">
      <div class="p-2">
        <div class="row">
          <div class="col-2">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="gameToAdd.name" required />
              <label for="floatingInput">Название</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select name="" id="" class="form-select" v-model="gameToAdd.developer_fk" required>
                <option :value="g.id" v-for="g in developer">{{ g.name }}</option>
              </select>
              <label for="floatingInput">Разработчик</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select name="" id="" class="form-select" v-model="gameToAdd.genre_fk">
                <option :value="g.id" v-for="g in genre">{{ g.name }}</option>
              </select>
              <label for="floatingInput">Жанр</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select name="" id="" class="form-select" v-model="gameToAdd.platform_fk">
                <option :value="g.id" v-for="g in platform">{{ g.name }}</option>
              </select>
              <label for="floatingInput">Платформа</label>
            </div>
          </div>
          <div class="col-auto" style="align-content: center; align-items: center;">
            <input class="form-control" type="file" ref="gamesPictureRef" @change="gamesAddPictureChange">
          </div>
          <div class="col-auto">
            <img :src="gamesAddImageUrl" style="max-height: 60px;" alt="">
          </div>
          <div class="d-grid gap-2 col-6 mx-auto g-2">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </div>
    </form>
    <div class="form-floating" v-if="isSuperUser === true">
      <select name="" id="" class="form-select" v-model="selectedUserId" @change="handleUserChange">
        <option :key="u.id" :value="u.id" v-for="u in users">{{ u.username }}</option>
      </select>
      <label for="floatingInput">Выберете пользователя</label>
    </div>
    <div class="stats-section" v-if="gameStats">
      <h3>Game Statistics</h3>
      <div>
        <p><strong>Количество записей:</strong> {{ gameStats.count }}</p>
      </div>
    </div>
    <label for="floatingInput">Выберите жанр</label>
    <div class="filter-item" style=" flex-grow: 1;">
      <select name="" id="" class="form-select" v-model="selectedGenreId" @change="handleGenreChange">
        <option :value="null">Выберете жанр</option>
        <option :value="g.id" v-for="g in genre">{{ g.name }}</option>
      </select>
    </div>
    <label for="floatingInput">Выберите платформу</label>
    <div class="filter-item" style="flex-grow: 1;">
      <select name="" id="" class="form-select" v-model="selectedPlatformId" @change="handlePlatformChange">
        <option :value="null">Выберете платформу</option>
        <option :value="g.id" v-for="g in platform">{{ g.name }}</option>
      </select>
    </div>
    <div class="d-flex justify-content-between align-items-center mb-2 ">
      <button @click="toggleSortOrder" class="btn btn-outline-primary btn-sm">
        Сортировать: {{ sortOrder === 'asc' ? 'A-Я' : 'Я-A' }}
      </button>
      <a href="#" @click="exportExcel" class="text-export">Экспорт в Excel</a>
    </div>
    <div>
      <div v-for="item in sortedGames" :key="item.id" class="games-item">
        <div>{{ item.name }}</div>
        <div>{{ delevoperById[item.developer_fk]?.name }}</div>
        <div>{{ genreById[item.genre_fk]?.name }}</div>
        <div>{{ platformById[item.platform_fk]?.name }}</div>
        <div v-show="item.picture">
          <img :src="item.picture" style="max-height: 60px;" alt="Game image" data-bs-toggle="modal"
            data-bs-target="#imageModal" @click="openImageModal(item.picture)">
        </div>
        <div>
          <button class="btn btn-success" @click="onEditClick(item)">
            <i class="bi bi-pencil"></i>
          </button>
        </div>
        <div>
          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>

      <div v-if="otpModalVisible" class="modal-overlay">
        <div class="modal-content">
          <h4>Введите OTP код</h4>
          <div class="form-floating">
            <input v-model="otpCode" type="text" class="form-control" id="otpInput" placeholder="Код OTP" required />
            <label for="otpInput">Код OTP</label>
          </div>
          <div class="d-grid gap-2 col-6 mx-auto g-2 mt-3">
            <button class="btn btn-primary" :disabled="isLoading" @click="verifyOtp">
              Проверка
            </button>
          </div>
          <div v-if="errorMessage" class="alert alert-danger mt-3">
            {{ errorMessage }}
          </div>
          <div v-if="successMessage" class="alert alert-success mt-3">
            {{ successMessage }}
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for viewing the image -->
    <div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="imageModalLabel">Изображение игры</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <img :src="selectedImageUrl" class="img-fluid" alt="Game image">
          </div>
        </div>
      </div>
    </div>

    <div v-if="editModalVisible" tabindex="-1" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              редактировать
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-flex">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="gameToEdit.name" />
                  <label for="floatingInput">Название</label>
                </div>
              </div>
              <div class="col-flex">
                <div class="form-floating">
                  <select name="" id="" class="form-select" v-model="gameToEdit.developer_fk">
                    <option :value="g.id" v-for="g in developer">{{ g.name }}</option>
                  </select>
                  <label for="floatingInput">Разработчик</label>
                </div>
              </div>
              <div class="col-flex">
                <div class="form-floating">
                  <select name="" id="" class="form-select" v-model="gameToEdit.genre_fk">
                    <option :value="g.id" v-for="g in genre">{{ g.name }}</option>
                  </select>
                  <label for="floatingInput">Жанр</label>
                </div>
              </div>
              <div class="col-flex">
                <div class="form-floating">
                  <select name="" id="" class="form-select" v-model="gameToEdit.platform_fk">
                    <option :value="g.id" v-for="g in platform">{{ g.name }}</option>
                  </select>
                  <label for="floatingInput">Платформа</label>
                </div>
              </div>
              <div class="row p-2">
                <div class="col-auto">
                  <input class="form-control" type="file" ref="editGamePictureRef" @change="gamesEditPictureChange">
                </div>
                <div class="col-auto">
                  <img :src="gamesEditImageUrl" style="max-height: 60px;" alt="Preview">
                </div>
              </div>
            </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Закрыть
            </button>
            <button type="button" class="btn btn-primary" @click="onUpdateGame">
              Сохранить
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style lang="css" scoped>
.games-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid purple;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr auto auto;
  gap: 16px;
  align-content: center;
  align-items: center;

}

.stats-section {
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}
</style>
