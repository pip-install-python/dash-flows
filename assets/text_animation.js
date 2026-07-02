/**
 * Claude-style Typewriter Animation for "Dash Docs"
 * Creates a streaming text effect similar to Claude's response animation
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Text animation handler loaded');

    // Configuration
    const TEXT_TO_TYPE = "Dash Docs";
    const TYPING_SPEED = 80; // milliseconds per character
    const INITIAL_DELAY = 500; // delay before starting animation

    // Function to get the title element
    function getTitleElement() {
        return document.getElementById('dash-docs-title');
    }

    // Function to type out text character by character
    function typeWriter(text, element, index = 0) {
        if (index < text.length) {
            // Add next character
            element.textContent = text.substring(0, index + 1);

            // Continue to next character
            setTimeout(() => typeWriter(text, element, index + 1), TYPING_SPEED);
        } else {
            // Animation complete - remove typing class
            element.classList.remove('typing');
            console.log('Typing animation complete');
        }
    }

    // Function to start the animation
    function startAnimation() {
        const titleElement = getTitleElement();

        if (titleElement) {
            // Clear text and add typing class for cursor
            titleElement.textContent = '';
            titleElement.classList.add('typing');

            // Start typing after initial delay
            setTimeout(() => {
                typeWriter(TEXT_TO_TYPE, titleElement);
            }, INITIAL_DELAY);

            console.log('Started text animation');
        } else {
            console.log('Title element not found');
        }
    }

    // Run animation on initial load
    startAnimation();

    // Re-run animation when navigating (for Dash SPA)
    const observer = new MutationObserver(function(mutations) {
        // Check if the title element was re-rendered
        const titleElement = getTitleElement();
        if (titleElement && titleElement.textContent === TEXT_TO_TYPE && !titleElement.dataset.animated) {
            // Mark as animated to prevent re-animation on same element
            titleElement.dataset.animated = 'true';

            // Clear and restart animation
            clearTimeout(window.titleAnimationTimeout);
            window.titleAnimationTimeout = setTimeout(startAnimation, 100);
        }
    });

    // Observe document for changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    console.log('Text animation observer active');
});
