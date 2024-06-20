#version 330
layout(origin_upper_left) in vec4 gl_FragCoord;


out vec4 FragColor;

void main() {
    FragColor = vec4(gl_FragCoord.x / 1920., gl_FragCoord.y / 1080., gl_FragCoord.z, 1.);
}