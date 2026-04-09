import { n as BaseComponent, t as publicDirURL } from "../../../public_dir-C5bujZKB.js";
import { t as colors } from "../../../helpers-B9BQYaS6.js";
import { dump, themes } from "@poppinss/dumper/html";
import { dump as dump$1 } from "@poppinss/dumper/console";
var ErrorCause = class extends BaseComponent {
	cssFile = new URL("./error_cause/style.css", publicDirURL);
	async toHTML(props) {
		if (!props.error.cause) return "";
		return `<section>
      <div class="card">
        <div class="card-heading">
          <div>
            <h3 class="card-title">
              Error Cause
            </h3>
          </div>
        </div>
        <div class="card-body">
          <div id="error-cause">
            ${dump(props.error.cause, {
			cspNonce: props.cspNonce,
			styles: themes.cssVariables,
			inspectObjectPrototype: false,
			inspectStaticMembers: false,
			inspectArrayPrototype: false
		})}
          </div>
        </div>
      </div>
    </section>`;
	}
	async toANSI(props) {
		if (!props.error.cause) return "";
		let depth = process.env.YOUCH_CAUSE ? Number(process.env.YOUCH_CAUSE) : 2;
		if (Number.isNaN(depth)) depth = 2;
		return `\n\n${colors.red("[CAUSE]")}\n${dump$1(props.error.cause, {
			depth,
			inspectObjectPrototype: false,
			inspectStaticMembers: false,
			inspectArrayPrototype: false
		})}`;
	}
};
export { ErrorCause };
