#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/pi/puppy_pi/src/third_party/navigation/base_local_planner"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/pi/puppy_pi/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/pi/puppy_pi/install/lib/python3/dist-packages:/home/pi/puppy_pi/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/pi/puppy_pi/build" \
    "/usr/bin/python3" \
    "/home/pi/puppy_pi/src/third_party/navigation/base_local_planner/setup.py" \
     \
    build --build-base "/home/pi/puppy_pi/build/third_party/navigation/base_local_planner" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/pi/puppy_pi/install" --install-scripts="/home/pi/puppy_pi/install/bin"
