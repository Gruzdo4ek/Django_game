import {defineStore} from "pinia"
import { onBeforeMount, ref} from "vue";
import axios from 'axios';

const useUserProfileStore = defineStore("userProfileStore", ()=>{
    const isAuthorized = ref();
    const username = ref();
    const isSuperUser = ref();

    onBeforeMount(async()=>{
        const r = await axios.get("/api/user-profile/info/");
        isAuthorized.value = r.data.is_authenticated
        username.value = r.data.username
        isSuperUser.value = r.data.is_superuser
    })
    return {isAuthorized, username, isSuperUser}
})
export default useUserProfileStore
