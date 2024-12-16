<script setup>
import { ref } from 'vue';
import axios from 'axios';  

// Создаем переменные для хранения введенного OTP и состояния загрузки/ошибок
const otpCode = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

// Функция для отправки OTP на сервер
const verifyOtp = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    // Отправляем запрос на сервер
    const response = await axios.post('/api/otp-login/', { otp_key: otpCode.value });

    if (response.data.success) {
      successMessage.value = 'OTP код успешно проверен!';
      // Здесь можно выполнить редирект или другие действия после успешной проверки
    } else {
      errorMessage.value = 'Неверный OTP код, попробуйте снова.';
    }
  } catch (error) {
    errorMessage.value = 'Произошла ошибка при проверке OTP. Попробуйте снова позже.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <div class="row">
        <div class="col-12 col-md-6">
          <!-- Форма для ввода OTP -->
          <div class="form-floating">
            <input
              v-model="otpCode"
              type="text"
              class="form-control"
              id="otpInput"
              placeholder="Код OTP"
              required
            />
            <label for="otpInput">Код OTP</label>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <!-- Кнопка для отправки OTP -->
          <div class="d-grid gap-2 col-6 mx-auto g-2">
            <button
              class="btn btn-primary"
              :disabled="isLoading"
              @click="verifyOtp"
            >
              Проверка
            </button>
          </div>
        </div>
      </div>

      <!-- Сообщения об ошибке или успехе -->
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="alert alert-success mt-3">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.container-fluid {
  margin-top: 50px;
}
</style>
