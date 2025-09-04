"""
GUI application for Erics-Omvandlare using tkinter.

Provides a simple interface for converting text to PDF and DOCX formats.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys
import io
import subprocess
import platform
from datetime import datetime
from converter import DocumentConverter
from pandoc_setup import setup_pandoc


class OmvandlareGUI:
    """Main GUI application for Erics-Omvandlare."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Erics omvandlare - Dokumentkonverterare")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Initialize converter
        self.converter = DocumentConverter()
        
        # Setup GUI components
        self.setup_gui()
        
        # Center the window
        self.center_window()
    
    def setup_gui(self):
        """Setup all GUI components."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Erics omvandlare", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Input label
        input_label = ttk.Label(main_frame, 
                               text="Klistra in från språkmodellen här:",
                               font=("Arial", 10))
        input_label.grid(row=1, column=0, columnspan=2, pady=(0, 5), sticky=tk.W)
        
        # Text area
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       pady=(0, 15))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Text input with scrollbar
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                  width=70, height=20,
                                                  font=("Consolas", 11))
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Text area starts empty - no placeholder text
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Export button (only DOCX)
        self.docx_button = ttk.Button(button_frame, text="📝 Exportera till Word", 
                                    command=self.export_to_docx, width=25)
        self.docx_button.grid(row=0, column=0, padx=(0, 15))
        
        # Clear button
        self.clear_button = ttk.Button(button_frame, text="🗑️ Rensa text", 
                                     command=self.clear_text, width=15)
        self.clear_button.grid(row=0, column=1, padx=(15, 0))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Redo - Klistra in text och klicka på exportera!")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, 
                              font=("Arial", 9))
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                       pady=(10, 0))
        
        # Format info
        info_label = ttk.Label(main_frame, 
                              text="Tips: Texten behandlas som Markdown-format. Använd Markdown-syntax för bästa resultat!",
                              font=("Arial", 8), foreground="gray")
        info_label.grid(row=5, column=0, columnspan=2, pady=(5, 0))
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def get_text_content(self):
        """Get the current text content from the text area."""
        return self.text_area.get("1.0", tk.END).strip()
    
    def generate_filename(self, extension):
        """Generate a default filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"converted_document_{timestamp}.{extension}"
    
    def capture_stderr_warnings(self, func, *args, **kwargs):
        """Capture stderr output from a function call to catch Pandoc warnings."""
        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = captured_stderr = io.StringIO()
        
        try:
            # Call the function
            result = func(*args, **kwargs)
            
            # Get any warnings from stderr
            warnings = captured_stderr.getvalue()
            
            return result, warnings
        
        finally:
            # Restore stderr
            sys.stderr = old_stderr
    
    def show_warnings_if_any(self, warnings_text):
        """Display warnings to the user if any were captured."""
        if warnings_text.strip():
            # Extract meaningful warnings (skip empty lines and minor notices)
            warning_lines = [line.strip() for line in warnings_text.split('\n') 
                           if line.strip() and '[WARNING]' in line]
            
            if warning_lines:
                # Format warnings for display
                formatted_warnings = "\n".join(warning_lines)
                
                # Translate common warnings to Swedish
                if "TeX math" in formatted_warnings:
                    swedish_msg = (
                        "Varning: Hittade problem med matematiska uttryck i texten.\n\n"
                        "Detta kan bero på:\n"
                        "• Ofullständiga LaTeX-matematikuttryck\n"
                        "• Saknade klammer eller parenteser\n"
                        "• Felaktig matematisk syntax\n\n"
                        f"Teknisk information:\n{formatted_warnings}\n\n"
                        "Dokumentet skapades ändå, men kontrollera det matematiska innehållet."
                    )
                else:
                    swedish_msg = (
                        "Varning: Några problem upptäcktes under konverteringen.\n\n"
                        f"{formatted_warnings}\n\n"
                        "Dokumentet skapades ändå, men kontrollera resultatet."
                    )
                
                messagebox.showwarning("Konverteringsvarningar", swedish_msg)
    
    def open_file(self, file_path):
        """Open a file with the default system application."""
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            messagebox.showwarning(
                "Kunde inte öppna filen", 
                f"Filen skapades framgångsrikt men kunde inte öppnas automatiskt.\n\n"
                f"Du kan öppna den manuellt: {file_path}\n\n"
                f"Teknisk information: {str(e)}"
            )
    
    def export_to_docx(self):
        """Export the text content to DOCX format."""
        try:
            # Get text content
            content = self.get_text_content()
            if not content:
                messagebox.showwarning("Inget innehåll", "Vänligen ange någon text att konvertera!")
                return
            
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".docx",
                initialfile=self.generate_filename("docx"),
                filetypes=[("Word-dokument", "*.docx"), ("Alla filer", "*.*")],
                title="Spara Word-dokument som..."
            )
            
            if not filename:
                return  # User cancelled
            
            # Update status
            self.status_var.set("Exporterar till Word...")
            self.root.update()
            
            # Convert and save with warning capture
            result, warnings = self.capture_stderr_warnings(
                self.converter.convert_text, 
                content, 'docx', 'markdown', output_file=filename
            )
            
            # Success message
            self.status_var.set(f"Framgångsrikt exporterat till: {os.path.basename(filename)}")
            
            # Show success dialog first
            messagebox.showinfo("Klart!", f"Word-dokument exporterat framgångsrikt!\n\nSparat som: {filename}")
            
            # Automatically open the created document
            self.open_file(filename)
            
            # Then show any warnings that were captured
            self.show_warnings_if_any(warnings)
            
        except Exception as e:
            self.status_var.set("Export misslyckades!")
            messagebox.showerror("Exportfel", f"Misslyckades med att exportera till Word:\n\n{str(e)}\n\nSe till att du har de nödvändiga beroendena installerade.")
    
    def clear_text(self):
        """Clear all text from the text area."""
        if messagebox.askyesno("Rensa text", "Är du säker på att du vill rensa all text?"):
            self.text_area.delete("1.0", tk.END)
            self.status_var.set("Text rensad - Redo för nytt innehåll!")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Main function to start the GUI application."""
    try:
        # Setup bundled pandoc path if running as frozen executable
        setup_pandoc()
        
        app = OmvandlareGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
