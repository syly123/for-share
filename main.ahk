; US to JIS

+6::+7
+7::'
'::+;
+;::+=
+8::+9
+9::+0
+0::+-
+'::+8
[::+2
]::[
\::]
+]::+[
+\::+]
`::vkF3
+[::`
+2::+'
+8:: {
    Send "+9"
}
+^Esc:: ExitApp ; Exit script with Escape key
vk1D:: {
    Send "{ click Down }"
    KeyWait "vk1D"
    Send "{ Click Up }"
    return
}
sc07B:: {
    Send "{ Click Down } "
    KeyWait "sc07B"
    Send "{ click Up }"
    return
}
sc070:: {
    Send "{vkF2}"
}
sc073:: {
    Send "{vkE2}"
}
vk1C:: {
    Send "+;"
}
vk1C & n:: {
    Send "."
}
vk1C & m:: {
    Send "."
}
vk1C & ,:: {
    Send "+:"
}
vk1C & .:: {
    Send "+:"
}
^@:: {
    Send "{F5}"
    Send "{Enter}"
}
^Enter:: {
    Send "{F2}"
    Send "^{Enter}"
    return
}
^!z UP:: {
    Send "{F2}"
    Sleep 100
    Send "^a"
    Send "^c"
    Send "{Enter}"
}
RShift Up:: {
    Send "{Enter}"
}
RShift & Tab:: {
    Send "+{Tab}"
}
control:: {
    Send "{F2}"
}
!LButton:: {
    Send "{Plus}"
}