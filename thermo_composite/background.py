"""Decorative viewport background for the Streamlit application."""

from __future__ import annotations

import streamlit as st


def render_composite_background() -> None:
    """Render the static, non-interactive textured background once per app run."""
    st.markdown(
        """
        <div class="tc-background" aria-hidden="true">
          <div class="tc-background__island"></div>
          <div class="tc-background__island tc-background__island--secondary"></div>
          <svg class="tc-background__filters" width="0" height="0" focusable="false">
            <filter id="tc-octave-one" x="-10%" y="-10%" width="120%" height="120%">
              <feTurbulence type="fractalNoise" baseFrequency="0.0004"
                numOctaves="8" seed="4" result="tc-o1"></feTurbulence>
              <feTurbulence type="fractalNoise" baseFrequency="0.0008"
                numOctaves="8" seed="4" result="tc-o2"></feTurbulence>
              <feTurbulence type="fractalNoise" baseFrequency="0.0001"
                numOctaves="8" seed="4" result="tc-o3"></feTurbulence>
              <feTurbulence type="fractalNoise" baseFrequency="0.0018"
                numOctaves="8" seed="4" result="tc-o4"></feTurbulence>
              <feMerge result="tc-final-one">
                <feMergeNode in="tc-o1"></feMergeNode>
                <feMergeNode in="tc-o3"></feMergeNode>
                <feMergeNode in="tc-o1"></feMergeNode>
                <feMergeNode in="tc-o3"></feMergeNode>
              </feMerge>
              <feGaussianBlur in="tc-final-one" stdDeviation="5"
                result="tc-noise-one"></feGaussianBlur>
              <feDiffuseLighting in="tc-noise-one" surfaceScale="12"
                diffuseConstant="1" lighting-color="#91a9ad" result="tc-lit-one">
                <feDistantLight azimuth="90" elevation="45"></feDistantLight>
              </feDiffuseLighting>
              <feBlend in="tc-lit-one" in2="SourceGraphic" mode="normal"></feBlend>
            </filter>
            <filter id="tc-octave-two" x="-10%" y="-10%" width="120%" height="120%">
              <feTurbulence type="fractalNoise" baseFrequency="0.0004"
                numOctaves="8" seed="7" result="tc-p1"></feTurbulence>
              <feTurbulence type="fractalNoise" baseFrequency="0.0008"
                numOctaves="8" seed="7" result="tc-p2"></feTurbulence>
              <feTurbulence type="fractalNoise" baseFrequency="0.0001"
                numOctaves="8" seed="7" result="tc-p3"></feTurbulence>
              <feTurbulence type="fractalNoise" baseFrequency="0.0018"
                numOctaves="8" seed="7" result="tc-p4"></feTurbulence>
              <feMerge result="tc-final-two">
                <feMergeNode in="tc-p2"></feMergeNode>
                <feMergeNode in="tc-p4"></feMergeNode>
                <feMergeNode in="tc-p1"></feMergeNode>
                <feMergeNode in="tc-p3"></feMergeNode>
              </feMerge>
              <feGaussianBlur in="tc-final-two" stdDeviation="5"
                result="tc-noise-two"></feGaussianBlur>
              <feDiffuseLighting in="tc-noise-two" surfaceScale="12"
                diffuseConstant="1" lighting-color="#7f999e" result="tc-lit-two">
                <feDistantLight azimuth="-90" elevation="45"></feDistantLight>
              </feDiffuseLighting>
              <feBlend in="tc-lit-two" in2="SourceGraphic" mode="normal"></feBlend>
            </filter>
          </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )
