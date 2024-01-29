```
<style>
:root {
--brand-color: #FF6A51;
--darkest-color: #29323E;
--dark-color: #3A4655;
--mid-color: #C4BC9D;
--light-color: #F1EEE2;
--lightest-color: #FFFFFF;
  }
</style>
```


```tailwind

// Add this to tailwind.config.js
const colors = require("tailwindcss/colors");

module.exports = {
  theme: {
    extend : {
      colors: {
        brand: "#FF6A51",
        darkest: "#29323E",
        dark: "#3A4655",
        mid: "#C4BC9D",
        light: "#F1EEE2",
        lightest: "#FFFFFF"
      },
    },
  },
};
```