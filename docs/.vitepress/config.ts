import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "DDSS",
    description: "Distributed Deductive System Sorts",
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            { text: "Home", link: "/" },
            { text: "Guide", link: "/intro" },
        ],

        sidebar: [
            {
                text: "Guide",
                items: [
                    { text: "Introduction", link: "/intro" },
                    { text: "Modules", link: "/modules" },
                    { text: "Installation", link: "/installation" },
                    { text: "Usage", link: "/usage" },
                ],
            },
            {
                text: "About",
                items: [{ text: "License & Links", link: "/license" }],
            },
        ],

        socialLinks: [{ icon: "github", link: "https://github.com/USTC-KnowledgeComputingLab/ddss" }],
    },
});
