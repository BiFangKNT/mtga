import { Rule } from "eslint";
import { JSONSchema4 } from "json-schema";

//#region lib/types.d.ts
type RuleListener = Rule.RuleListener;
interface RuleModule {
  meta: RuleMetaData;
  create(context: Rule.RuleContext): RuleListener;
}
type RuleCategory = "Possible Errors" | "Best Practices" | "Stylistic Issues";
type SeverityString = "error" | "warn" | "off";
interface RuleMetaData {
  docs: {
    description: string;
    category: RuleCategory;
    recommended: boolean;
    url: string;
    ruleId: string;
    ruleName: string;
    default?: Exclude<SeverityString, "off">;
  };
  messages: {
    [messageId: string]: string;
  };
  fixable?: "code" | "whitespace";
  schema: JSONSchema4 | JSONSchema4[];
  deprecated?: boolean;
  replacedBy?: string[];
  type: "problem" | "suggestion" | "layout";
  hasSuggestions?: boolean;
}
//#endregion
//#region lib/configs/rules/recommended.d.ts
declare const rules$2: Record<string, SeverityString>;
declare namespace recommended_d_exports {
  export { plugins$1 as plugins, rules$2 as rules };
}
declare const plugins$1: {
  readonly regexp: {
    configs: {
      recommended: typeof recommended_d_exports;
      all: typeof all_d_exports;
      "flat/all": typeof all_d_exports;
      "flat/recommended": typeof recommended_d_exports;
    };
    rules: {
      [key: string]: RuleModule;
    };
    meta: {
      name: string;
      version: string;
    };
  };
};
//#endregion
//#region lib/configs/rules/all.d.ts
declare const rules$1: {
  [x: string]: SeverityString;
};
declare namespace all_d_exports {
  export { plugins, rules$1 as rules };
}
declare const plugins: {
  readonly regexp: {
    configs: {
      recommended: typeof recommended_d_exports;
      all: typeof all_d_exports;
      "flat/all": typeof all_d_exports;
      "flat/recommended": typeof recommended_d_exports;
    };
    rules: {
      [key: string]: RuleModule;
    };
    meta: {
      name: string;
      version: string;
    };
  };
};
//#endregion
//#region lib/index.d.ts
declare const meta: {
  name: string;
  version: string;
};
declare const configs: {
  recommended: typeof recommended_d_exports;
  all: typeof all_d_exports;
  "flat/all": typeof all_d_exports;
  "flat/recommended": typeof recommended_d_exports;
};
declare const rules: {
  [key: string]: RuleModule;
};
declare const regexp: {
  configs: {
    recommended: typeof recommended_d_exports;
    all: typeof all_d_exports;
    "flat/all": typeof all_d_exports;
    "flat/recommended": typeof recommended_d_exports;
  };
  rules: {
    [key: string]: RuleModule;
  };
  meta: {
    name: string;
    version: string;
  };
};
//#endregion
export { configs, regexp as default, meta, rules };