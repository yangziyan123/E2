document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("home-posts");

    console.log("home.js loaded");

    fetch("/api/posts")
        .then(res => res.json())
        .then(posts => {
            // 最新三篇（按 id 倒序）
            posts = posts.sort((a, b) => b.id - a.id).slice(0, 3);

            container.innerHTML = "";

            if (posts.length === 0) {
                container.innerHTML = "<p>暂无文章。</p>";
                return;
            }

            posts.forEach(post => {
                const card = document.createElement("div");
                card.className = "home-card";

                card.innerHTML = `
                    <div class="home-title">${post.title}</div>

                    <div class="home-excerpt">
                        ${post.content ? post.content.slice(0, 80) + "..." : "（无内容）"}
                    </div>

                    <div class="home-meta">
                        状态：${post.status}
                    </div>
                `;

                card.addEventListener("click", () => {
                    window.location.href = "/static/post.html?id=" + post.id;
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("加载失败:", err);
            container.innerHTML = "<p>加载失败，请检查 API。</p>";
        });
});
