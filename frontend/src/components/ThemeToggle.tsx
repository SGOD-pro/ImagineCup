import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTheme } from "@/hooks/useTheme";

export const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleTheme}
      className="h-9 w-9 rounded-lg transition-colors hover:bg-muted"
    >
      {theme === "dark" ? (
        <Sun className="h-4 w-4 text-wisteria" />
      ) : (
        <Moon className="h-4 w-4 text-bright-lavender" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
};
