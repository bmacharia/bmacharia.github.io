import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Cloud Native Musings: A DevOps Journal",
    pageTitleSuffix: " | babumacharia.com",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "en-US",
    baseUrl: "babumacharia.com",
    ignorePatterns: ["private", "templates", ".obsidian", "05_Templates", "00_Index", "01_Source", "02_Notes", "03-Concepts", "04_Synthesis", "06_Blog_Drafts", "07_Blog_Drafts", "08_Export", "09_Automation"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "JetBrains Mono",
        body: "Inter",
        code: "JetBrains Mono",
      },
      colors: {
        // "Dress Whites" — crisp navy-on-white with brass gold accents
        lightMode: {
          light: "#f5f8fc",
          lightgray: "#dce4f0",
          gray: "#5b6b8c",
          darkgray: "#17233d",
          dark: "#0a1830",
          secondary: "#1857c9",
          tertiary: "#c99a2e",
          highlight: "rgba(24, 87, 201, 0.08)",
          textHighlight: "#ffd54f55",
        },
        // "Dress Blues" — deep navy with bright signal-blue and brass gold accents
        darkMode: {
          light: "#0a1830",
          lightgray: "#16233f",
          gray: "#7c8fb3",
          darkgray: "#d7e1f2",
          dark: "#f5f8fc",
          secondary: "#4fa3ff",
          tertiary: "#ffc94a",
          highlight: "rgba(79, 163, 255, 0.12)",
          textHighlight: "#ffc94a44",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.ExplicitPublish()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
