async (page) => {
  const root = '/var/folders/nf/x69g9nlx2834r7zs_52xykj80000gn/T/specforge-regression-nqm71b3n/E-16-phase2/output/playwright/';
  const url = 'http://127.0.0.1:8876/app.html';
  const checks = [];
  const check = (name, ok, evidence = '') => {
    checks.push({name, passed: Boolean(ok), evidence});
    if (!ok) throw new Error(JSON.stringify(checks, null, 2));
  };
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const layout = () => page.evaluate(() => {
    const cards = [...document.querySelectorAll('.piece')];
    const zoom = parseFloat(getComputedStyle(document.documentElement).zoom) || 1;
    return {
      width: innerWidth,
      overflow: document.documentElement.scrollWidth > innerWidth,
      columns: getComputedStyle(document.getElementById('collection')).gridTemplateColumns.split(' ').length,
      cards: cards.map(card => {
        const heading = card.querySelector('h2');
        const summary = card.querySelector('.summary');
        const button = card.querySelector('button');
        const h = heading.getBoundingClientRect();
        const s = summary.getBoundingClientRect();
        const b = button.getBoundingClientRect();
        const c = card.getBoundingClientRect();
        return {
          titleClamped: h.height / zoom <= parseFloat(getComputedStyle(heading).lineHeight) * 2 + 1,
          summaryClamped: s.height / zoom <= parseFloat(getComputedStyle(summary).lineHeight) * 3 + 1,
          clearAction: b.top >= s.bottom && b.right <= c.right && b.left >= c.left,
          target: b.height >= 44,
        };
      }),
    };
  });
  await page.goto(url);
  await page.setViewportSize({width:1440,height:1000});
  check('原有藏品保留且不添加虚构正式数据', await page.locator('.piece').count() === 1 && await page.locator('.piece h2').textContent() === '一件需要较长标题才能说明来历的藏品');
  check('缺失说明列表显示暂无说明', await page.locator('.summary').textContent() === '暂无说明');
  await page.screenshot({path: root + 'list-1440.png', fullPage:true});
  await page.keyboard.press('Tab');
  check('键盘进入查看入口且焦点可见', await page.evaluate(() => document.activeElement.id === 'view-item-001' && getComputedStyle(document.activeElement).outlineStyle === 'solid'));
  await page.keyboard.press('Enter');
  check('原藏品详情完整且缺失说明正确', await page.locator('#detail-view').isVisible() && await page.locator('#detail-title').textContent() === '一件需要较长标题才能说明来历的藏品' && await page.locator('#detail-description').textContent() === '暂无说明');
  await page.keyboard.press('Shift+Tab');
  check('键盘可到达返回入口且焦点可见', await page.evaluate(() => document.activeElement.id === 'back' && getComputedStyle(document.activeElement).outlineStyle === 'solid'));
  await page.keyboard.press('Enter');
  await page.waitForFunction(() => !document.getElementById('list-view').hidden);
  check('键盘返回恢复原入口焦点', await page.evaluate(() => document.activeElement.id === 'view-item-001'));

  const longTitle = '虚构测试：这是一件需要完整叙述来源、保存过程与个人记忆的藏品，连续长标题也应保持入口清楚。'.repeat(5);
  const longDescription = '虚构测试：这段文字只用于检查长说明的摘要、详情与换行。完整原文应当保留，不因卡片省略而丢失。'.repeat(12) + '\n\n第二段：阅读结束后，返回原来的位置继续翻阅。';
  const fixtures = [
    {id:'short',title:'虚构测试：一封旧信',description:'虚构测试：一个简短的说明。'},
    {id:'original',title:'一件需要较长标题才能说明来历的藏品',description:longDescription},
    {id:'long',title:longTitle,description:longDescription},
    {id:'missing',title:'虚构测试：无说明藏品',description:''},
    ...Array.from({length:8}, (_,i) => ({id:'extra-'+i,title:'虚构测试：浏览样本 '+(i+1),description:'虚构测试：用于验证滚动位置恢复。'})),
  ];
  let samples = fixtures;
  await page.route('**/app.html', async route => {
    const response = await route.fetch();
    const html = await response.text();
    await route.fulfill({response, body:html.replace(/(<script id="collection-data" type="application\/json">)[\s\S]*?(<\/script>)/, '$1' + JSON.stringify(samples) + '$2')});
  });
  for (const [width, height, columns] of [[1440,1000,3],[768,1000,2],[375,812,1]]) {
    await page.setViewportSize({width,height});
    await page.goto(url);
    const result = await layout();
    check(width + 'px 混合文本排版', !result.overflow && result.columns === columns && result.cards.every(card => card.titleClamped && card.summaryClamped && card.clearAction && card.target), result);
    if (width === 375 || width === 768) await page.screenshot({path:root+'mixed-'+width+'.png',fullPage:true});
    else await page.screenshot({path:root+'mixed-1440.png',fullPage:true});
    await page.locator('#view-long').click();
    check(width + 'px 详情保留完整标题说明', await page.locator('#detail-title').textContent() === longTitle && await page.locator('#detail-description').textContent() === longDescription);
    check(width + 'px 详情不横向溢出', await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    if (width === 1440 || width === 375) await page.screenshot({path:root+'detail-'+width+'.png',fullPage:true});
    await page.locator('#back').click();
    await page.waitForFunction(() => !document.getElementById('list-view').hidden);
  }
  const beforeOrder = await page.locator('.piece h2').allTextContents();
  await page.locator('#view-extra-5').scrollIntoViewIfNeeded();
  const scrollBefore = await page.evaluate(() => window.scrollY);
  await page.locator('#view-extra-5').click();
  await page.goBack();
  await page.waitForFunction(() => !document.getElementById('list-view').hidden);
  check('浏览器后退恢复滚动位置与焦点', await page.evaluate(y => Math.abs(window.scrollY-y) <= 1 && document.activeElement.id === 'view-extra-5', scrollBefore), {scrollBefore,scrollAfter:await page.evaluate(() => scrollY)});
  check('返回后内容顺序不变', JSON.stringify(beforeOrder) === JSON.stringify(await page.locator('.piece h2').allTextContents()));
  await page.goForward();
  check('浏览器前进重开同一藏品', await page.locator('#detail-title').textContent() === '虚构测试：浏览样本 6');
  await page.locator('#back').click();
  await page.waitForFunction(() => !document.getElementById('list-view').hidden);

  for (const width of [1440,768,375]) {
  await page.setViewportSize({width,height:1000});
  await page.goto(url);
  await page.evaluate(() => document.documentElement.style.zoom = '2');
  const zoomed = await layout();
  check(width + 'px / 200% CSS 放大无横向溢出且入口可见', !zoomed.overflow && zoomed.cards.every(card => card.titleClamped && card.summaryClamped && card.clearAction && card.target), zoomed);
  if (width === 768) await page.screenshot({path:root+'list-zoom-200.png',fullPage:true});
  await page.locator('#view-long').click();
  check(width + 'px / 200% 放大可阅读详情并返回', await page.locator('#detail-description').textContent() === longDescription && await page.locator('#back').isVisible() && await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  if (width === 768) await page.screenshot({path:root+'detail-zoom-200.png',fullPage:true});
  await page.locator('#back').click();
  await page.waitForFunction(() => !document.getElementById('list-view').hidden);
  check(width + 'px / 200% 返回恢复入口焦点', await page.evaluate(() => document.activeElement.id === 'view-long'));
  await page.evaluate(() => document.documentElement.style.zoom = '');
  }

  await page.goto(url+'#collection/long');
  await page.locator('#back').click();
  check('直接打开详情仍可返回列表', await page.locator('#list-view').isVisible() && !page.url().includes('#'));
  await page.goto(url+'#collection/nonexistent');
  check('无效藏品地址安全回到列表', await page.locator('#list-view').isVisible());

  samples = [];
  for (const width of [1440,375]) {
    await page.setViewportSize({width,height:900});
    await page.goto(url);
    check(width + 'px 空收藏无无效操作', await page.locator('#empty').isVisible() && await page.locator('#list-view button').count() === 0 && await page.locator('.piece').count() === 0);
    await page.screenshot({path:root+'empty-'+width+'.png',fullPage:true});
  }
  await page.unroute('**/app.html');
  await page.goto(url);
  await page.setViewportSize({width:1440,height:1000});
  check('正式集合恢复为原有单件藏品', await page.locator('.piece').count() === 1 && await page.locator('.piece h2').textContent() === '一件需要较长标题才能说明来历的藏品');
  check('无 JavaScript 运行错误', errors.length === 0, errors);
  return JSON.stringify(checks, null, 2);
}
