import { FullSlug, resolveRelative } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

interface NavItem {
  label: string
  slug: FullSlug
}

const navItems: NavItem[] = [
  { label: "Home", slug: "index" as FullSlug },
  { label: "Blog", slug: "Blog" as FullSlug },
  { label: "Projects", slug: "HomeLab/Projects" as FullSlug },
  { label: "About", slug: "HomeLab/About" as FullSlug },
  { label: "Contact", slug: "HomeLab/Contact" as FullSlug },
]

const Navigation: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const currentSlug = fileData.slug!
  return (
    <nav class={classNames(displayClass, "nav-menu")}>
      <ul>
        {navItems.map((item, i) => (
          <li>
            <a href={resolveRelative(currentSlug, item.slug)} class="internal">
              {item.label}
            </a>
            {i < navItems.length - 1 && <span class="nav-sep">|</span>}
          </li>
        ))}
      </ul>
    </nav>
  )
}

Navigation.css = `
.nav-menu {
  font-family: var(--codeFont);
  font-size: 0.9rem;
  flex: auto;
}

.nav-menu ul {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 0.5rem;
}

.nav-menu li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-menu a {
  color: var(--dark);
  text-decoration: none;
}

.nav-menu a:hover {
  color: var(--secondary);
}

.nav-menu .nav-sep {
  color: var(--gray);
}
`

export default (() => Navigation) satisfies QuartzComponentConstructor
