// uniform vec3 color;
varying vec3 vColor;

void main() {
    float strength = distance(gl_PointCoord, vec2(0.5));
    strength = step(0.5, strength);
    strength = 1.0 - strength;
    gl_FragColor = vec4(vColor, strength);
    // gl_FragColor = vec4(0.2431, 0.0039, 0.9608, 1.0);
}
