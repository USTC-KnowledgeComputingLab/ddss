import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "DDSS",
    description: "Distributed Deductive System Sorts",

    // 多语言配置
    locales: {
        root: {
            label: "English",
            lang: "en",
        },
        zh: {
            label: "简体中文",
            lang: "zh-CN",
            link: "/zh/",
            themeConfig: {
                nav: [
                    { text: "首页", link: "/zh/" },
                    { text: "指南", link: "/zh/intro" },
                ],
                sidebar: [
                    {
                        text: "指南",
                        items: [
                            { text: "简介", link: "/zh/intro" },
                            { text: "模块", link: "/zh/modules" },
                            { text: "安装", link: "/zh/installation" },
                            { text: "使用", link: "/zh/usage" },
                        ],
                    },
                    {
                        text: "关于",
                        items: [{ text: "许可与链接", link: "/zh/license" }],
                    },
                ],
                // 中文特有的配置
                docFooter: {
                    prev: "上一页",
                    next: "下一页",
                },
                outline: {
                    label: "页面导航",
                },
            },
        },
    },

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
