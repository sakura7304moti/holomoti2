<template>
  <q-avatar size="lg"> <img :src="user.userImage" /> </q-avatar
  ><span class="q-ml-sm">{{ user.userName }}</span>
</template>
<script lang="ts">
import { computed, defineComponent } from 'vue';
export default defineComponent({
  name: 'user-icon',
  props: {
    state: {
      type: Object as () => User,
      required: true,
    },
  },
  setup(props) {
    const user = computed(() => props.state);
    return { user };
  },
});
interface User {
  userId: string;
  userImage: string;
  userName: string;
}
</script>
