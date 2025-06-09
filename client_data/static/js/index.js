$(document).ready(function () {
  const $form = $('#client-form');
  const $sections = $('.form-section');
  const $formMessages = $('#form-messages');
  const $messageList = $('#form-messages ul');
  let currentSection = 0;

  function initForm() {
    $sections.each(function (index) {
      const $section = $(this);
      $section.find('.form-content').toggle(index === 0);
      $section.find('.section-toggle').text(index === 0 ? '-' : '+');
    });
    setupEventListeners();
  }

  function setupEventListeners() {
    $('.section-toggle').on('click', toggleSection);
    $form.on('submit', handleSubmit);

    $('#meeting_status').on('change', function () {
      $('#other-status-field').toggle($(this).val() === 'other');
    });

    $('#industry').on('change', function () {
      $('#other-industry-field').toggle($(this).val() === 'Other');
    });

    $('#product').on('change', function () {
      $('#other_product').closest('.other-field').toggle($(this).val() === 'other');
    });

    $('input[name="deal_status"]').on('change', function () {
      $('#other-deal-field').toggle($(this).val() === 'other');
    });

    $('input[name="provider"]').on('change', function () {
      $('#other-provider-field').toggle($(this).val() === 'other');
    });

    $('input[name="net_connected"]').on('change', function () {
      $('#net_section').toggle($(this).val() === 'yes');
    });
  }

  function toggleSection() {
    const $button = $(this);
    const $section = $button.closest('.form-section');
    const $content = $section.find('.form-content');

    $content.toggle();
    $button.text($content.is(':visible') ? '-' : '+');
  }

  function validateSection(index) {
    const $section = $($sections[index]);
    const $inputs = $section.find('input, select, textarea');
    let isValid = true;

    $messageList.empty();
    $formMessages.hide();

    $inputs.each(function () {
      const $input = $(this);
      if ($input.prop('required') && !$input.val().trim()) {
        isValid = false;
        const labelText = $input.closest('.form-group').find('label').first().text() || 'This field';
        addValidationMessage(`${labelText} is required.`);
      }
    });

    if (!isValid) {
      $formMessages.show();
    }
    return isValid;
  }

  function addValidationMessage(message) {
    $('<li>').text(message).appendTo($messageList);
  }

  function handleSubmit(e) {
    e.preventDefault();

    let isValid = true;
    $messageList.empty();
    $formMessages.hide();

    $sections.each(function (index) {
      if (!validateSection(index)) {
        isValid = false;
      }
    });

    if (!isValid) {
      $formMessages.show();
      return;
    }

    alert('Form submitted successfully! Data would be processed on a real server.');
    $form[0].reset();

    $('.other-field').hide();
    $('#net_section').hide();
    currentSection = 0;
    initForm();
  }

  initForm();
});
