---
# This is a redirection page to the default language
---

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vitepress";

const { go } = useRouter();

onMounted(() => {
  go("/ddss/en/");
});
</script>
