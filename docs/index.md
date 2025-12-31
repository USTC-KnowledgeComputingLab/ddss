---
# This is a redirection page to the default language
---

<script setup>
import { onMounted } from "vue";
import { useRouter, withBase } from "vitepress";

const { go } = useRouter();

onMounted(() => {
  const userLang = navigator.language || navigator.userLanguage;
  if (userLang.toLowerCase().startsWith("zh")) {
    go(withBase("/zh/"));
  } else {
    go(withBase("/en/"));
  }
});
</script>
