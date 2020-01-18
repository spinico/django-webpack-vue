// SPDX-License-Identifier: MIT

import "./assets/styles/app";

//////////////////// Bootstrap ////////////////////

// Bootstrap - Complete
//import "bootstrap";

// Bootstrap - Components
import "bootstrap/js/dist/alert";
import "bootstrap/js/dist/button";
//import "bootstrap/js/dist/carousel";
import "bootstrap/js/dist/collapse";
import "bootstrap/js/dist/dropdown";
//import "bootstrap/js/dist/modal";
//import "bootstrap/js/dist/popover";
//import "bootstrap/js/dist/scrollspy";
//import "bootstrap/js/dist/tab";
//import "bootstrap/js/dist/toast";
//import "bootstrap/js/dist/tooltip";
//import "bootstrap/js/dist/util";

/////////////////// Font-Awesome ///////////////////

import { library, dom } from "@fortawesome/fontawesome-svg-core";

// Using single icon import to minimize bundle size
import { faBars } from "@fortawesome/free-solid-svg-icons/faBars";
import { faCheck } from "@fortawesome/free-solid-svg-icons/faCheck";
import { faCog } from "@fortawesome/free-solid-svg-icons/faCog";
import { faCogs } from "@fortawesome/free-solid-svg-icons/faCogs";
import { faPen } from "@fortawesome/free-solid-svg-icons/faPen";
import { faSyncAlt } from "@fortawesome/free-solid-svg-icons/faSyncAlt";
import { faCircleNotch } from "@fortawesome/free-solid-svg-icons/faCircleNotch";

library.add(faBars, faCheck, faCog, faCogs, faPen, faSyncAlt, faCircleNotch);

// Without dom.watch(), automatic replacement of Font-Awesome icons won't work in the rendered page
dom.watch();

/////////////////////// Theme //////////////////////

import { changeTheme } from "themes-switch";

((): void => {
  const items = document.getElementsByClassName("change-theme-menu-item");

  Array.from(items).forEach(function(element) {
    element.addEventListener("click", function(event) {
      const name = element.getAttribute("rel");
      changeTheme(name, "static/styles/themes/theme-" + name + ".css");
    });
  });

  function setTheme(name: string): void {
    localStorage.setItem("theme", name);
    document.documentElement.className = name;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const themeSlider = document.getElementById("theme-slider");

    if (localStorage.getItem("theme") === "theme-dark") {
      setTheme("theme-dark");
    } else {
      setTheme("theme-light");
    }

    // Toggle between light and dark theme
    themeSlider!.addEventListener("click", function(event) {
      if (localStorage.getItem("theme") === "theme-dark") {
        setTheme("theme-light");
      } else {
        setTheme("theme-dark");
      }
    });
  });
})();
