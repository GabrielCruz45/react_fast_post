import {useState} from "react"

function ThemeInput({onSubmit}) {
    const [theme, setTheme] = useState("");
    const [theme, setTheme] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!theme.trim()) {
            setError("Please enter a theme name.");
            return;
        };

        onSubmit(theme);
    }


    return <div className="input-theme-container">
        <h2>Generate your adventure</h2>
        <p>Enter a theme for your interactive story</p>

        <form onSubmit={handleSubmit}>
            <div className="input-group">
                <input 
                    type="text"
                    value={theme}
                    onChange={(e) => setTheme(e.target.value)}
                    placeholder="Enter a theme. (e.g. fantasy, space, pirates, medieval)"
                    className={error ? 'error' : ''}
                />
                {error && <p className="error-text">{error}</p>}
            </div>
            <button type="submit" className="generate-btn">
                Generate Story
            </button>
        </form>
    </div>;
};

export default ThemeInput;