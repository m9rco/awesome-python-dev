/* Progressive enhancements: every resource and navigation link works without JS. */
(() => {
  "use strict";

  const controls = document.querySelector(".catalog-controls");
  const search = document.getElementById("tool-search");
  const kind = document.getElementById("kind-filter");
  const installable = document.getElementById("installable-only");
  const cards = Array.from(document.querySelectorAll(".tool-card"));
  const resultCount = document.getElementById("result-count");
  const noResults = document.getElementById("no-results");
  const normalized = (value) => value.normalize("NFKC").toLocaleLowerCase().trim();

  if (controls && search && cards.length) {
    const index = cards.map((card) => ({
      card,
      text: normalized(card.dataset.name || card.textContent),
      kind: card.dataset.kind,
      installable: card.dataset.installable === "true",
    }));
    const filter = () => {
      const terms = normalized(search.value).split(/\s+/).filter(Boolean);
      const selectedKind = kind ? kind.value : "";
      let count = 0;
      index.forEach((entry) => {
        const matches = terms.every((term) => entry.text.includes(term)) &&
          (!selectedKind || selectedKind === "all" || entry.kind === selectedKind) &&
          (!(installable && installable.checked) || entry.installable);
        entry.card.hidden = !matches;
        if (matches) count += 1;
      });
      if (resultCount) {
        const defaultLabel = document.documentElement.lang.startsWith("zh") ?
          "显示 {count} / {total} 项资源" : "{count} of {total} resources";
        const template = resultCount.dataset.label || defaultLabel;
        resultCount.textContent = template.replace("{count}", count).replace("{total}", cards.length);
      }
      if (noResults) noResults.hidden = count > 0;
    };
    controls.hidden = false;
    search.addEventListener("input", filter);
    if (kind) kind.addEventListener("change", filter);
    if (installable) installable.addEventListener("change", filter);
    filter();
  }

  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    if (!document.getElementById(button.dataset.copyTarget)) return;
    button.hidden = false;
    let reset;
    button.addEventListener("click", async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      if (!target) return;
      const original = button.dataset.label || button.textContent;
      button.dataset.label = original;
      clearTimeout(reset);
      try {
        await navigator.clipboard.writeText(target.textContent.trim());
        button.textContent = button.dataset.copied || "Copied!";
      } catch {
        button.textContent = button.dataset.error || "Select the command to copy";
      }
      reset = setTimeout(() => { button.textContent = original; }, 2400);
    });
  });
})();
