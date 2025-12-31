---
# This is a redirection page to the default language
---

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vitepress";

const { go } = useRouter();

onMounted(() => {
  const userLang = navigator.language || navigator.userLanguage;
  if (userLang.toLowerCase().startsWith("zh")) {
    go("./zh/");
  } else {
    go("./en/");
  }
});
</script>
