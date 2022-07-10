<script setup>
const props = defineProps({
    color: {
        type: String,
        default: '#00a6ed',
        validator: value => RegExp('^#[0-9a-f]{6}$').test(value),
    },
    background: {
        type: String,
        default: '#f3f3f3',
        validator: value => RegExp('^#[0-9a-f]{6}$').test(value),
    },
    size: {
        type: Number,
        default: 120,
        validator: value => value > 0,
    },
    thickness: {
        type: Number,
        default: 16,
        validator: value => value > 0,
    },
    radius: {
        type: Number,
        default: 50,
        validator: value => value > 0,
    },
    speed: {
        type: Number,
        default: 2,
        validator: value => value > 0,
    },
    animationType: {
        type: String,
        default: 'linear',
        validator: value => ['ease-in-out', 'ease-in', 'ease-out', 'linear'].includes(value),
    },
    message: {
        type: String,
        default: '',
    },
})

const { color, background, size, thickness, radius, speed, animationType, message } = props;

const style = {
    'width': `${size}px`,
    'height': `${size}px`,
    'border-radius': `${radius}%`,
    'border': `${thickness}px solid ${background}`,
    'border-top': `${thickness}px solid ${color}`,
    'animation': `spin ${speed}s ${animationType} infinite`,
};

</script>

<template>
    <div class="loader">
        <div :style="style"></div>
        <span :v-if="message.length > 0" class="loader-title">{{ message }}</span>
    </div>>
</template>

<style>
.loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.70);
    z-index: 9999;
}

.loader>.loader-title {
    font-size: 1.5rem;
    color: #fff;
    margin-top: 1rem;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>