/**
 * Auth gate card — Clerk sign-in / sign-up triggers.
 *
 * The interactive gate (lib/gate_layouts.py) renders "Sign in" /
 * "Create free account" buttons with static IDs. Clicks are delegated at the
 * document level so the listeners survive Dash re-renders.
 *
 * Satellite mode: Clerk FORBIDS its modal here ("This operation is not
 * allowed on a satellite domain") — it only auto-syncs an existing session,
 * it never initiates one. So on a satellite we NAVIGATE to the primary
 * (window.dashClerkAuth.buildSatelliteRedirect(), dash-clerk-auth ≥ 0.9.2:
 * primary /onboarding?returnTo=<here>), which signs the user in and sends
 * them straight back. The modal remains the non-satellite/local-dev path.
 *
 * Coexistence: lib/auth.py's capture-phase fixup owns #clerk-login-button
 * (the package's own widget); this file owns only #auth-gate-*. Disjoint
 * selectors, same destination — both return to the current page.
 */
document.addEventListener("click", (e) => {
    const signup = e.target.closest("#auth-gate-signup");
    const signin = e.target.closest("#auth-gate-signin");
    if (!signup && !signin) return;

    const here = window.location.href;
    const dca = window.dashClerkAuth;
    if (dca && dca.isSatellite) {
        // Needs no ClerkJS at all — works even while clerk.browser.js loads.
        const dest = dca.buildSatelliteRedirect
            ? dca.buildSatelliteRedirect(signup ? { mode: "signup" } : {})
            : null;
        if (dest) {
            window.location.assign(dest);
            return;
        }
        if (window.Clerk && window.Clerk.redirectToSignIn) {
            if (signup && window.Clerk.redirectToSignUp) {
                window.Clerk.redirectToSignUp({ signUpForceRedirectUrl: here });
            } else {
                window.Clerk.redirectToSignIn({ signInForceRedirectUrl: here });
            }
            return;
        }
        console.warn("[auth-gate] satellite mode but no redirect target and Clerk JS not loaded");
        return;
    }

    if (!window.Clerk) {
        console.warn("[auth-gate] Clerk JS not loaded — cannot open auth flow");
        return;
    }

    const opts = {
        redirectUrl: here,
        afterSignInUrl: here,
        afterSignUpUrl: here,
    };

    if (signup) {
        window.Clerk.openSignUp(opts);
    } else {
        window.Clerk.openSignIn(opts);
    }
});
