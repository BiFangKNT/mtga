import { n as BaseComponent, t as publicDirURL } from "../../../public_dir-C5bujZKB.js";
import { n as htmlEscape } from "../../../helpers-B9BQYaS6.js";
import { dump, themes } from "@poppinss/dumper/html";
var ErrorMetadata = class extends BaseComponent {
	cssFile = new URL("./error_metadata/style.css", publicDirURL);
	#primitives = [
		"string",
		"boolean",
		"number",
		"undefined"
	];
	#formatRowValue(value, dumpValue, cspNonce) {
		if (dumpValue === true) return dump(value, {
			styles: themes.cssVariables,
			cspNonce
		});
		if (this.#primitives.includes(typeof value) || value === null) return typeof value === "string" ? htmlEscape(value) : value;
		return dump(value, {
			styles: themes.cssVariables,
			cspNonce
		});
	}
	#renderRows(rows, cspNonce) {
		return `<table class="card-table">
      <tbody>
        ${rows.map((row) => {
			return `<tr>
              <td class="table-key">${row.key}</td>
              <td class="table-value">
                ${this.#formatRowValue(row.value, row.dump, cspNonce)}
              </td>
            </tr>`;
		}).join("\n")}
      </tbody>
    </table>`;
	}
	#renderSection(section, rows, cspNonce) {
		return `<div>
      <h4 class="card-subtitle">${section}</h4>
      ${Array.isArray(rows) ? this.#renderRows(rows, cspNonce) : `<span>${this.#formatRowValue(rows.value, rows.dump, cspNonce)}</span>`}
    </div>`;
	}
	#renderGroup(group, sections, cspNonce) {
		return `<section class="metadata-group">
      <div class="card">
        <div class="card-heading">
          <h3 class="card-title">${group}</h3>
        </div>
        <div class="card-body">
          ${Object.keys(sections).map((section) => this.#renderSection(section, sections[section], cspNonce)).join("\n")}
        </div>
      </div>
    </section>`;
	}
	async toHTML(props) {
		const groups = props.metadata.toJSON();
		const groupsNames = Object.keys(groups);
		if (!groupsNames.length) return "";
		return groupsNames.map((group) => this.#renderGroup(group, groups[group], props.cspNonce)).join("\n");
	}
	async toANSI() {
		return "";
	}
};
export { ErrorMetadata };
