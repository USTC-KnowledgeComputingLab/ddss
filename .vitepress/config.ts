import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
    base: "/ddss/",
    title: "DDSS",
    description: "Distributed Deductive System Sorts",
    srcDir: "docs",

    locales: {
        en: {
            label: "English",
            lang: "en",
            link: "/en/",
            themeConfig: {
                nav: [
                    { text: "Home", link: "/en/" },
                    { text: "Guide", link: "/en/intro" },
                ],
                sidebar: [
                    {
                        text: "Guide",
                        items: [
                            { text: "Introduction", link: "/en/intro" },
                            { text: "Modules", link: "/en/modules" },
                            { text: "Installation", link: "/en/installation" },
                            { text: "Usage", link: "/en/usage" },
                        ],
                    },
                    {
                        text: "About",
                        items: [{ text: "License & Links", link: "/en/license" }],
                    },
                ],
                footer: {
                    message: "Released under the GNU Affero General Public License v3.0 or later.",
                    copyright: "Copyright © 2025-present Hao Zhang",
                },
            },
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
                docFooter: {
                    prev: "上一页",
                    next: "下一页",
                },
                outline: {
                    label: "页面导航",
                },
                footer: {
                    message: "基于 GNU Affero General Public License v3.0 或更高版本发布。",
                    copyright: "版权所有 © 2025-至今 张浩",
                },
            },
        },
    },

    themeConfig: {
        search: { provider: "local" },
        socialLinks: [{ icon: "github", link: "https://github.com/USTC-KnowledgeComputingLab/ddss" }],
    },
});
