import { createContext, useState, useMemo } from "react";
import { createTheme } from "@mui/material/styles";

// color design tokens export
export const tokens = (mode) => ({
  ...(mode === "dark"
    ? {
        grey: {
          100: "#e0e0e0",
          200: "#c2c2c2",
          300: "#a3a3a3",
          400: "#858585",
          500: "#666666",
          600: "#525252",
          700: "#3d3d3d",
          800: "#292929",
          900: "#141414",
        },
        primary: {
          100: "#d6eaff",
          200: "#add5ff",
          300: "#85c0ff",
          400: "#5caaFF",
          500: "#1B9CFC",  // Neon blue
          600: "#0087e5",
          700: "#0070bf",
          800: "#005999",
          900: "#004274",
        },
        greenAccent: {
          100: "#dbfdfd",
          200: "#b7fafa",
          300: "#94f6f6",
          400: "#70f3f3",
          500: "#18ffff",  // Neon cyan
          600: "#00cccc",
          700: "#009999",
          800: "#006666",
          900: "#003333",
        },
        background: {
          default: "#121212",  // Dark background
          paper: "#1e1e1e",    // Dark paper for cards, panels
        },
        text: {
          primary: "#ffffff",  // White text for contrast
          secondary: "#a0a0a0",  // Grey text for secondary elements
        },
      }
    : {
        // Light mode colors can go here
      }),
});

// Create Material-UI theme
export const themeSettings = (mode) => {
  const colors = tokens(mode);

  return {
    palette: {
      mode: mode,
      primary: {
        main: colors.primary[500],
      },
      secondary: {
        main: colors.greenAccent[500],
      },
      background: {
        default: colors.background.default,
        paper: colors.background.paper,
      },
      text: {
        primary: colors.text.primary,
        secondary: colors.text.secondary,
      },
    },
    typography: {
      fontFamily: ["Roboto", "sans-serif"].join(","),
      fontSize: 12,
      h1: {
        fontFamily: ["Roboto", "sans-serif"].join(","),
        fontSize: 40,
      },
      h2: {
        fontFamily: ["Roboto", "sans-serif"].join(","),
        fontSize: 32,
      },
      h3: {
        fontFamily: ["Roboto", "sans-serif"].join(","),
        fontSize: 24,
      },
      h4: {
        fontFamily: ["Roboto", "sans-serif"].join(","),
        fontSize: 20,
      },
      h5: {
        fontFamily: ["Roboto", "sans-serif"].join(","),
        fontSize: 16,
      },
      h6: {
        fontFamily: ["Roboto", "sans-serif"].join(","),
        fontSize: 14,
      },
    },
  };
};

// Context for the color mode (light/dark toggle)
export const ColorModeContext = createContext({
  toggleColorMode: () => {},
});

export const useMode = () => {
  const [mode, setMode] = useState("dark");

  const colorMode = useMemo(
    () => ({
      toggleColorMode: () =>
        setMode((prev) => (prev === "light" ? "dark" : "light")),
    }),
    []
  );

  const theme = useMemo(() => createTheme(themeSettings(mode)), [mode]);
  return [theme, colorMode];
};
