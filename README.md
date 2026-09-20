# mimar-skills

Türkiye kamu yapıları için Claude skill'leri:

- **[mimar-sinan](./mimar-sinan/)** — mimari proje mevzuat denetimi ve m² ihtiyaç programı
- **[birim-fiyat](./birim-fiyat/)** — keşif (yaklaşık maliyet), poz eşleştirme, fiyat analizi, hakediş, fiyat farkı; Excel giriş/çıkış

Yapı, [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) yazım standardını izler: SKILL.md ≤10 KB, referanslar ayrı, stdlib-only Python araçları, güven etiketli bulgular.

```
/plugin marketplace add damnali17-ops/mimar-skills
/plugin install mimar-sinan@mimar-skills
/plugin install birim-fiyat@mimar-skills
```

MIT.
