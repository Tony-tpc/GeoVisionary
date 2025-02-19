/**
 * 获取随机ID
 * @param {*} length
 * @returns
 */
const COLORS = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399']
function getRandomNum(min: number, max: number) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function randomColor() {
  return COLORS[getRandomNum(0, 4)]
}

const website = 'https://wanderprints.com'
// const website = 'https://www.getphotoblanket.com';

export const getList = ({ page = 1, pageSize = 20 }) => {

  const imageModules = import.meta.glob('/public/models/images/*.{jpeg,png}', {
    eager: true,
    import: 'default'
  });

  const dynamicProducts = Object.values(imageModules).map((imgPath, index) => ({
    id: imgPath.split('/').pop().replace(/\.jpe?g$/, ''),
    star: false,
    src: { original: imgPath },
    backgroundColor: randomColor(),
    name: `${imgPath
      .split('/').pop()
      .replace(/\.jpe?g$/, '')
      .replace(/([a-z])([A-Z])/g, '\$1 \$2') // 处理驼峰命名
      .replace(/[_-]/g, ' ')               // 替换所有分隔符为空格
      .toLowerCase()
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')}`
  }));
  console.log(dynamicProducts);

  return Promise.resolve(dynamicProducts);
}


