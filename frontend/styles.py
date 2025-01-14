def get_theme_css(theme):
    themes = {
        'light': """
            .stApp {
                background-color: #ffffff;
                color: #000000;
            }
        """,
        'dark': """
            .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }
        """,
        'custom': """
            .stApp {
                background-color: #1a1a1a;
                color: #00ff00;
            }
            .stButton>button {
                background-color: #004d00;
                color: #ffffff;
            }
        """
    }
    return themes.get(theme.lower(), themes['dark']) 