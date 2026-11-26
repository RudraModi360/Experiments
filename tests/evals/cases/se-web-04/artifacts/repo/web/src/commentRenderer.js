export function renderComment(comment) {
  // BUG: raw interpolation allows XSS and javascript: hrefs
  const link = comment.authorUrl ? `<a href="${comment.authorUrl}">${comment.author}</a>` : comment.author;
  return `<div class="comment"><strong>${link}</strong><p>${comment.body}</p></div>`;
}
