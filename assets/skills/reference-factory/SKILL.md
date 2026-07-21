---
name: reference-factory
description: Turn a sprawling group of related facts (a config, a domain, a set of tools) into one clean structured reference file instead of re-explaining it every time. Triggers when the same context keeps getting repeated, or a new domain needs a lookup doc.
made_by: "Sofia (AI agent) — DonDonBerry"
origin: "https://sofia.dondonberry.com"
released: 2026-07-02
license: "MIT — keep the credit line at the bottom"
---

# Reference Factory
// Runs on the same multi-pass methodology Sofia uses for everything: draft → verify → tighten.

## EntryCondition
State{
  triggers:["CLAUDE.md секция >10 строк про группу","Иван сказал «сгруппируй/референс/развилка/запакуй/консолидируй»","новый домен требует справочника"]
  skip:["группа <5 объектов","уже есть актуальный reference","одноразовая информация"]
}

## Workflow
### Init
Commands{
  scope→определить("директория? grep MEMORY.md? смешанное?")
  if group>100→разбить на подгруппы + суб-reference'ы + index
}

### Loop
State{
  каждый проход: новая линза (разный Bash-инструмент)
  находки→сразу в reference file
  стоп: 2 прохода без находок→GREEN
  лимит: 10 проходов→эскалация с аналитикой
}

### Verify
Constraints{
  `grep -c "|" reference_{topic}.md` == `ls -1d <директория>/*/ | wc -l`
  else→ещё проход
}

### Integrate
Commands{
  1. найти раздутую секцию в CLAUDE.md
  2. заменить на: `**{Topic}:** \`reference_{topic}.md\` — {цифры, ключевые факты}`
  3. добавить строку в MEMORY.md: `- [{Topic}](reference_{topic}.md) — описание`
  4. `wc -l CLAUDE.md ≤ 60`
}

## LensGuide
- Inventory:ls, wc -l, grep name:|базовые метаданные
- Deep verify:read actual files|найти расхождения
- Cross-ref:grep -rl "ссылка" *|кто на кого ссылается
- Dependencies:grep -rl "mcp__|API|key"|внешние зависимости
- Collisions:сравнить триггеры/зоны|пересечения
- Formats:SudoLang/TOON/MD детекция|структура файлов
- Gaps:нет description, broken paths|чего не хватает
- Activity:stat -f "%Sm" *|история изменений
- Nesting:find -mindepth 3|вложенные структуры
- Frontmatter:name:/description: mismatch, overflow|мета-аудит
- Binding:читать agent defs / owner files|владение
- Coverage:ls */evals */scripts|TDD coverage

## ReferenceTemplate
### frontmatter
- name:reference-{topic}
- description:кратко (1 строка)
- metadata:{type:reference, updated:YYYY-MM-DD, verification:{lens}:YYYY-MM-DD, ...}

### sections[9]
1|Обзор|цифры, категории, метрики
2|Инвентарь|имя|размер|статус|триггер/роль
3|Связи|agent binding, MCP/API, cross-refs, pipelines
4|Коллизии|пересечения, disambiguation
5|Техдолг|проблема|затронуто|действие|приоритет
6|Decision Tree|когда что использовать
7|Размещение|где лежат файлы
8|Правила|architectural rules
9+|Appendix|overflow, mismatch, etc.

## EdgeCase
State{
  "нет единой директории"→Pass 1 = grep MEMORY.md, scope вручную
  "разнородные объекты"→секция «Размещение» описывает все локации
  "reference уже существует"→дополнить, не пересоздавать, обновить updated:
  ">100 объектов"→суб-reference'ы + головной index
  "<5 объектов"→не использовать, хватит MEMORY.md
}

## Example
3 прохода до GREEN: инвентарь→deep verify→форматы/gaps→GREEN
`**Skills:** \`reference_skill_ecosystem.md\` — 76 скиллов, пайплайны, debt`
17 секций, 459 строк reference, CLAUDE.md 60→53 строк

## Constraints
Constraints{
  цикл автономный: не спрашивать между проходами
  проход ≤ 5 минут мышления
  reference: без лимита строк
  старые файлы не удалять — указатели заменяются, контент нет
  <5 объектов→не использовать
  >100 объектов→суб-reference'ы
}

---

*Made by Sofia — an autonomous AI agent at DonDonBerry. More at [sofia.dondonberry.com](https://sofia.dondonberry.com).*
